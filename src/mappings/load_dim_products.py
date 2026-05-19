from pathlib import Path
import pandas as pd
import duckdb


MAPPING_PATH = Path("data/mappings/biedronka_products.csv")
DB_PATH = "data/warehouse/warehouse.db"


mapping_df = pd.read_csv(
    MAPPING_PATH,
    sep=";"
)

print("\n=== CSV CHECK ===")
print(mapping_df.head())
print(mapping_df.shape)

print("\n=== NULL CHECK ===")
print(mapping_df.isnull().sum())


con = duckdb.connect(DB_PATH)

con.register("mapping_temp", mapping_df)

con.execute("""
CREATE OR REPLACE TABLE dim_products AS
SELECT * FROM mapping_temp
""")


print("\n=== DIM_PRODUCTS CHECK ===")

print(
    con.execute("""
    SELECT *
    FROM dim_products
    LIMIT 10
    """).fetchdf()
)