from pathlib import Path
import pandas as pd
import duckdb

from src.parsers.lidl_txt_parser import parse_lidl_files
from src.parsers.biedronka_json_parser import parse_biedronka_files


DB_PATH = "data/warehouse/warehouse.db"


# ==========================
# MAIN PIPELINE STEP
# ==========================
def run_bronze_ingestion():

    con = duckdb.connect(DB_PATH)

    # ==========================
    # BEFORE METRICS
    # ==========================
    before_receipts = con.execute("""
        SELECT COUNT(*) FROM bronze_receipts
    """).fetchone()[0]

    before_items = con.execute("""
        SELECT COUNT(*) FROM bronze_receipts_items
    """).fetchone()[0]

    # ==========================
    # EXTRACT + TRANSFORM
    # ==========================
    print("\nLoading raw receipts...")

    lidl_receipts, lidl_items = parse_lidl_files(
        Path("data/raw/lidl")
    )

    biedronka_receipts, biedronka_items = parse_biedronka_files(
        Path("data/raw/biedronka/json")
    )

    receipts_df = pd.DataFrame(lidl_receipts + biedronka_receipts)
    items_df = pd.DataFrame(lidl_items + biedronka_items)

    receipts_df["date"] = pd.to_datetime(
        receipts_df["date"],
        utc=True
    ).dt.tz_convert(None)

    # ==========================
    # LOAD (BRONZE)
    # ==========================
    load_to_duckdb(con, receipts_df, items_df)

    # ==========================
    # AFTER METRICS
    # ==========================
    after_receipts = con.execute("""
        SELECT COUNT(*) FROM bronze_receipts
    """).fetchone()[0]

    after_items = con.execute("""
        SELECT COUNT(*) FROM bronze_receipts_items
    """).fetchone()[0]

    # ==========================
    # METRICS
    # ==========================
    new_receipts = after_receipts - before_receipts
    new_items = after_items - before_items

    print("\n=== BRONZE INGESTION METRICS ===")
    print(f"New receipts: {new_receipts}")
    print(f"New items: {new_items}\n")
    print(f"Total receipts: {after_receipts}")
    print(f"Total items: {after_items}")

    con.close()


# ==========================
# LOAD LAYER
# ==========================
def load_to_duckdb(con, receipts_df, items_df):

    # --------------------------
    # RECEIPTS
    # --------------------------
    con.register("receipts_temp", receipts_df)

    con.execute("""
        INSERT INTO bronze_receipts
        SELECT *
        FROM receipts_temp t
        WHERE NOT EXISTS (
            SELECT 1
            FROM bronze_receipts b
            WHERE b.receipt_id = t.receipt_id
        )
    """)

    # --------------------------
    # ITEMS
    # --------------------------
    con.register("items_temp", items_df)

    con.execute("""
        INSERT INTO bronze_receipts_items
        SELECT
            t.receipt_id,
            t.raw_name,
            NULL AS product_id,
            t.quantity,
            t.unit_price,
            t.total_price,
            t.discount,
            t.final_price
        FROM items_temp t
        WHERE NOT EXISTS (
            SELECT 1
            FROM bronze_receipts_items b
            WHERE b.receipt_id = t.receipt_id
              AND b.raw_name = t.raw_name
              AND b.total_price = t.total_price
        )
    """)


# ==========================
# ENTRYPOINT
# ==========================
if __name__ == "__main__":
    run_bronze_ingestion()