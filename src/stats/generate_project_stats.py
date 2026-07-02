from pathlib import Path
import json
import duckdb


def generate_project_stats():

    DB_PATH = "data/warehouse/warehouse.db"

    OUTPUT_PATH = Path(
        "data/stats/project_stats.json"
    )

    con = duckdb.connect(DB_PATH)

    stats = {

        "data_freshness": con.execute("""
            SELECT CAST(MAX(date) AS DATE)
            FROM bronze_receipts
        """).fetchone()[0].isoformat(),

        "receipts": con.execute("""
            SELECT COUNT(*)
            FROM bronze_receipts
        """).fetchone()[0],

        "products": con.execute("""
            SELECT COUNT(*)
            FROM bronze_receipts_items
        """).fetchone()[0],

        "stores": con.execute("""
            SELECT COUNT(DISTINCT store)
            FROM bronze_receipts
        """).fetchone()[0]

    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            stats,
            f,
            indent=4
        )

    print("\nProject statistics updated.")

    con.close()


if __name__ == "__main__":
    generate_project_stats()