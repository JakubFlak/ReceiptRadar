from pathlib import Path
import duckdb

def run_gold_models():

    DB_PATH = "data/warehouse/warehouse.db"

    with duckdb.connect(DB_PATH) as con:

        gold_folder = Path("sql/gold")

        for sql_file in sorted(gold_folder.glob("*.sql")):
            print(f"Running {sql_file.name}")

            query = sql_file.read_text(encoding="utf-8")
            con.execute(query)