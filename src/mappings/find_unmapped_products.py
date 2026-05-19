from pathlib import Path
import pandas as pd
import duckdb



DB_PATH = "data/warehouse/warehouse.db"

MAPPING_PATH = Path(
    "data/mappings/biedronka_products.csv"
)


con = duckdb.connect(DB_PATH)


def sync_dim_products(connection, mapping_frame):
    connection.register("mapping_temp", mapping_frame)
    connection.execute("""
    CREATE OR REPLACE TABLE dim_products AS
    SELECT * FROM mapping_temp
    """)


# ==========================================
# Find unmapped products
# ==========================================

unmapped_df = con.execute("""
SELECT DISTINCT
    br.store,
    bri.raw_name

FROM bronze_receipts_items bri

LEFT JOIN bronze_receipts br
    ON bri.receipt_id = br.receipt_id

LEFT JOIN dim_products dp
    ON LOWER(TRIM(bri.raw_name))
        = LOWER(TRIM(dp.raw_name))
    AND LOWER(TRIM(br.store))
        = LOWER(TRIM(dp.store))

WHERE dp.raw_name IS NULL

ORDER BY bri.raw_name
""").fetchdf()

print("\n=== UNMAPPED PRODUCTS ===")
print(unmapped_df)


# ==========================================
# Stop if nothing new
# ==========================================

if unmapped_df.empty:
    print("\nNo new unmapped products found.")
    exit()


# ==========================================
# Load existing mapping CSV
# ==========================================

mapping_df = pd.read_csv(
    MAPPING_PATH,
    sep=";"
)


# ==========================================
# Append only truly new rows
# ==========================================

new_rows_df = unmapped_df.merge(
    mapping_df[["store", "raw_name"]],
    on=["store", "raw_name"],
    how="left",
    indicator=True
)

new_rows_df = (
    new_rows_df[new_rows_df["_merge"] == "left_only"]
    .drop(columns=["_merge"])
    .copy()
)

if new_rows_df.empty:
    sync_dim_products(con, mapping_df)
    print("\nDIM_PRODUCTS refreshed from CSV.")
    print("\nNo new unmapped products found after CSV deduplication.")
    exit()

new_rows_df["clean_name"] = ""
new_rows_df["category"] = ""
new_rows_df["subcategory"] = ""

combined_df = pd.concat(
    [mapping_df, new_rows_df],
    ignore_index=True
)


# ==========================================
# Save updated CSV
# ==========================================

combined_df.to_csv(
    MAPPING_PATH,
    sep=";",
    index=False
)

sync_dim_products(con, combined_df)


print("\n=== MAPPING CSV UPDATED ===")
print(f"Added {len(new_rows_df)} new products.")
print("DIM_PRODUCTS refreshed from CSV.")
