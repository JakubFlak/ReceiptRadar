from pathlib import Path
import hashlib
import pandas as pd
import duckdb


def build_product_id(row: pd.Series) -> str:
    existing = str(row.get("product_id", "") or "").strip()
    if existing:
        return existing

    store = str(row.get("store", "") or "").strip().lower()
    raw_name = str(row.get("raw_name", "") or "").strip()
    clean_name = str(row.get("clean_name", "") or "").strip() or raw_name
    key = f"{store}|{raw_name}|{clean_name}".encode("utf-8")
    return "p_" + hashlib.sha1(key).hexdigest()[:12]


def read_mapping_df(mapping_path: Path) -> pd.DataFrame:
    for sep in [",", ";"]:
        try:
            df = pd.read_csv(mapping_path, sep=sep, encoding="utf-8-sig")
        except Exception:
            continue

        if not df.empty and len(df.columns) > 1:
            df.columns = [col.strip().lower() for col in df.columns]
            if "product_id" not in df.columns:
                df["product_id"] = ""
            df["product_id"] = df.apply(build_product_id, axis=1)
            return df

    raise ValueError(f"Could not parse mapping file: {mapping_path}")


def backfill_bronze_product_ids(con: duckdb.DuckDBPyConnection) -> None:
    columns = con.execute("PRAGMA table_info('bronze_receipts_items')").fetchall()
    if not any(col[1] == "product_id" for col in columns):
        con.execute("ALTER TABLE bronze_receipts_items ADD COLUMN product_id VARCHAR")

    con.execute("""
        UPDATE bronze_receipts_items AS bri
        SET product_id = (
            SELECT dp.product_id
            FROM dim_products AS dp
            JOIN bronze_receipts AS br
                ON br.receipt_id = bri.receipt_id
            WHERE LOWER(TRIM(bri.raw_name)) = LOWER(TRIM(dp.raw_name))
              AND LOWER(TRIM(br.store)) = LOWER(TRIM(dp.store))
            LIMIT 1
        )
        WHERE bri.product_id IS NULL OR bri.product_id = ''
    """)


def load_dim_products():

    MAPPING_PATH = Path("data/mappings/products.csv")
    DB_PATH = "data/warehouse/warehouse.db"

    mapping_df = read_mapping_df(MAPPING_PATH)

    print("Mapped products:", len(mapping_df))

    mapping_df.to_csv(MAPPING_PATH, index=False)

    con = duckdb.connect(DB_PATH)

    con.register("mapping_temp", mapping_df)

    con.execute("""
        CREATE OR REPLACE TABLE dim_products AS
        SELECT * FROM mapping_temp
    """)

    backfill_bronze_product_ids(con)

    con.close()