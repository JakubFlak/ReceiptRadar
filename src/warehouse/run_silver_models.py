from pathlib import Path
import duckdb


DB_PATH = "data/warehouse/warehouse.db"

SQL_PATH = Path(
    "sql/silver/silver_receipt_items.sql"
)


con = duckdb.connect(DB_PATH)

with open(SQL_PATH, "r") as f:
    query = f.read()

con.execute(query)

print(
    con.execute("""
    SELECT *
    FROM silver_receipt_items
    LIMIT 10
    """).fetchdf()
)

print(
    con.execute("""
    SELECT DISTINCT raw_name
    FROM silver_receipt_items
    WHERE clean_name IS NULL
    """).fetchdf()
)