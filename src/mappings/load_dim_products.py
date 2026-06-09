from pathlib import Path
import pandas as pd
import duckdb


def load_dim_products():
    MAPPING_PATH = Path("data/mappings/biedronka_products.csv")
    DB_PATH = "data/warehouse/warehouse.db"


    mapping_df = pd.read_csv(
        MAPPING_PATH,
        sep=";"
    )

    print("Mapped products: ", len(mapping_df))


    con = duckdb.connect(DB_PATH)

    con.register("mapping_temp", mapping_df)

    con.execute("""
    CREATE OR REPLACE TABLE dim_products AS
    SELECT * FROM mapping_temp
    """)