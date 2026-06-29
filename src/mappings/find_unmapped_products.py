from pathlib import Path
import pandas as pd
import duckdb

from src.mappings.load_dim_products import read_mapping_df, build_product_id


# ==========================
# MAIN ENTRYPOINT
# ==========================
def find_unmapped_products():

    DB_PATH = "data/warehouse/warehouse.db"
    MAPPING_PATH = Path("data/mappings/products.csv")

    with duckdb.connect(DB_PATH) as con:

        # 1. detect
        unmapped_df = get_unmapped_products(con)

        print(f"Unmapped products: {len(unmapped_df)}")

        # 2. load mapping
        mapping_df = read_mapping_df(MAPPING_PATH)

        # 3. update mapping CSV
        updated_mapping_df = update_mapping_csv(unmapped_df, mapping_df, MAPPING_PATH)

        # 4. refresh dim table
        sync_dim_products(con, updated_mapping_df)

        print("\n=== MAPPING UPDATED ===")
        print(f"Mapping size: {len(updated_mapping_df)}")


# ==========================
# DETECTION LAYER
# ==========================
def get_unmapped_products(con):

    return con.execute("""
        SELECT DISTINCT
            br.store,
            bri.raw_name
        FROM bronze_receipts_items bri
        LEFT JOIN bronze_receipts br
            ON bri.receipt_id = br.receipt_id
        LEFT JOIN dim_products dp
            ON bri.product_id = dp.product_id
        WHERE COALESCE(bri.product_id, '') = ''
           OR dp.product_id IS NULL
        ORDER BY bri.raw_name
    """).fetchdf()


# ==========================
# MAPPING LAYER
# ==========================
def update_mapping_csv(unmapped_df, mapping_df, mapping_path):

    if unmapped_df.empty:
        return mapping_df

    new_rows_df = unmapped_df.merge(
        mapping_df[["store", "raw_name"]],
        on=["store", "raw_name"],
        how="left",
        indicator=True
    )

    new_rows_df = new_rows_df[new_rows_df["_merge"] == "left_only"].drop(columns=["_merge"])

    if new_rows_df.empty:
        return mapping_df

    new_rows_df["clean_name"] = ""
    new_rows_df["category"] = ""
    new_rows_df["subcategory"] = ""
    new_rows_df["product_id"] = new_rows_df.apply(build_product_id, axis=1)

    combined_df = pd.concat([mapping_df, new_rows_df], ignore_index=True)

    combined_df.to_csv(mapping_path, sep=",", index=False)

    return combined_df


# ==========================
# LOADER LAYER
# ==========================
def sync_dim_products(con, mapping_df):

    con.register("mapping_temp", mapping_df)

    con.execute("""
        CREATE OR REPLACE TABLE dim_products AS
        SELECT * FROM mapping_temp
    """)