import duckdb

DB_PATH = "data/warehouse/warehouse.db"

def create_bronze_tables():
    con = duckdb.connect(DB_PATH)

    con.execute("""
    CREATE TABLE IF NOT EXISTS bronze_receipts (
        receipt_id VARCHAR,
        date TIMESTAMP,
        store VARCHAR
    )
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS bronze_receipts_items (
        receipt_id VARCHAR,
        raw_name VARCHAR,
        quantity DOUBLE,
        unit_price DOUBLE,
        total_price DOUBLE,
        discount DOUBLE,
        final_price DOUBLE
    )
    """)