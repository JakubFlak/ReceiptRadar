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
        product_id VARCHAR,
        quantity DOUBLE,
        unit_price DOUBLE,
        total_price DOUBLE,
        discount DOUBLE,
        final_price DOUBLE
    )
    """)

    columns = con.execute("PRAGMA table_info('bronze_receipts_items')").fetchall()
    if not any(col[1] == "product_id" for col in columns):
        con.execute("ALTER TABLE bronze_receipts_items ADD COLUMN product_id VARCHAR")