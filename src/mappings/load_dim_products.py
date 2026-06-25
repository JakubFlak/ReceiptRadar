from pathlib import Path
import pandas as pd
import duckdb


def read_mapping_df(mapping_path: Path) -> pd.DataFrame:
    for sep in [",", ";"]:
        try:
            df = pd.read_csv(mapping_path, sep=sep, encoding="utf-8-sig")
        except Exception:
            continue

        if not df.empty and len(df.columns) > 1:
            df.columns = [col.strip().lower() for col in df.columns]
            return df

    raise ValueError(f"Could not parse mapping file: {mapping_path}")


def load_dim_products():

    MAPPING_PATH = Path("data/mappings/products.csv")
    DB_PATH = "data/warehouse/warehouse.db"

    mapping_df = read_mapping_df(MAPPING_PATH)

    print("Mapped products:", len(mapping_df))

    con = duckdb.connect(DB_PATH)

    con.register("mapping_temp", mapping_df)

    con.execute("""
        CREATE OR REPLACE TABLE dim_products AS
        SELECT * FROM mapping_temp
    """)

    con.close()