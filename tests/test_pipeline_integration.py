import shutil
from pathlib import Path

import duckdb

from src.pipeline.run_pipeline import run_pipeline


def test_run_pipeline_on_isolated_test_data(tmp_path, monkeypatch):
    root = tmp_path
    (root / "data" / "raw" / "lidl").mkdir(parents=True, exist_ok=True)
    (root / "data" / "raw" / "biedronka" / "json").mkdir(parents=True, exist_ok=True)
    (root / "data" / "mappings").mkdir(parents=True, exist_ok=True)
    (root / "data" / "warehouse").mkdir(parents=True, exist_ok=True)
    (root / "sql" / "silver").mkdir(parents=True, exist_ok=True)
    (root / "sql" / "gold").mkdir(parents=True, exist_ok=True)

    (root / "data" / "raw" / "lidl" / "receipt1.txt").write_text(
        "2024-01-02\n"
        "Shop\n"
        "nr: 123 10:30\n"
        "Bread\n"
        "2 * 1.50 3.00\n",
        encoding="utf-8",
    )
    (root / "data" / "raw" / "biedronka" / "json" / "receipt2.json").write_text(
        '{"IDZ": "r002", "header": [{"headerData": {"date": "2024-01-03"}}], "body": [{"sellLine": {"name": "Milk 2l", "quantity": "1,0", "price": 250, "total": 250}}]}',
        encoding="utf-8",
    )
    (root / "data" / "mappings" / "products.csv").write_text(
        "store,raw_name,clean_name,category,subcategory\n"
        "biedronka,Milk,Milk,Dairy,Milk\n"
        "lidl,Bread,Bread,Bakery,Bread\n",
        encoding="utf-8",
    )

    repo_root = Path(__file__).resolve().parents[1]
    shutil.copytree(repo_root / "sql" / "silver", root / "sql" / "silver", dirs_exist_ok=True)
    shutil.copytree(repo_root / "sql" / "gold", root / "sql" / "gold", dirs_exist_ok=True)

    monkeypatch.chdir(root)

    run_pipeline()

    with duckdb.connect(str(root / "data" / "warehouse" / "warehouse.db")) as con:

        receipt_count = con.execute("SELECT COUNT(*) FROM bronze_receipts").fetchone()[0]
        item_count = con.execute("SELECT COUNT(*) FROM bronze_receipts_items").fetchone()[0]
        unmapped_count = con.execute(
            "SELECT COUNT(*) FROM bronze_receipts_items WHERE product_id IS NULL OR product_id = ''"
        ).fetchone()[0]

        assert receipt_count >= 2
        assert item_count >= 2
        assert unmapped_count == 0
