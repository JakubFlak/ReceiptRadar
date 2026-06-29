import duckdb


def test_bronze_data_quality_rules(tmp_path):
    db_path = tmp_path / "warehouse.db"
    with duckdb.connect(db_path) as con:

        con.execute(
            """
            CREATE TABLE bronze_receipts (
                receipt_id VARCHAR,
                date TIMESTAMP,
                store VARCHAR
            )
            """
        )
        con.execute(
            """
            CREATE TABLE bronze_receipts_items (
                receipt_id VARCHAR,
                raw_name VARCHAR,
                product_id VARCHAR,
                quantity DOUBLE,
                unit_price DOUBLE,
                total_price DOUBLE,
                discount DOUBLE,
                final_price DOUBLE
            )
            """
        )

        con.execute(
            """
            INSERT INTO bronze_receipts VALUES
                ('r1', '2024-01-01', 'biedronka'),
                ('r2', '2024-01-02', 'lidl')
            """
        )
        con.execute(
            """
            INSERT INTO bronze_receipts_items VALUES
                ('r1', 'Milk', 'p_1', 1.0, 2.50, 2.50, 0.0, 2.50),
                ('r2', 'Bread', 'p_2', 2.0, 1.50, 3.00, 0.0, 3.00)
            """
        )

        duplicate_receipt_ids = con.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT receipt_id
                FROM bronze_receipts
                GROUP BY receipt_id
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]
        assert duplicate_receipt_ids == 0

        null_required_fields = con.execute(
            """
            SELECT COUNT(*)
            FROM bronze_receipts_items
            WHERE receipt_id IS NULL
            OR raw_name IS NULL
            OR product_id IS NULL
            """
        ).fetchone()[0]
        assert null_required_fields == 0

        bad_values = con.execute(
            """
            SELECT COUNT(*)
            FROM bronze_receipts_items
            WHERE final_price < 0
            OR quantity <= 0
            OR unit_price <= 0
            """
        ).fetchone()[0]
        assert bad_values == 0
