from pathlib import Path
import duckdb


DB_PATH = "data/warehouse/warehouse.db"

SQL_PATH = Path(
    "sql/gold/gold_category_spending.sql"
)


con = duckdb.connect(DB_PATH)

with open(SQL_PATH, "r") as f:
    query = f.read()

con.execute(query)

print(
    con.execute("""
    SELECT *
    FROM gold_category_spending
    """).fetchdf()
)