from pathlib import Path
import json
import pandas as pd
import duckdb
from src.utils.product_cleaning import clean_raw_name

def load_biedronka():
    DATA_PATH = Path("data/raw/biedronka/json")
    DB_PATH = "data/warehouse/warehouse.db"


    def parse_receipt(data):

        header_data = next(
            h["headerData"] for h in data["header"]
            if "headerData" in h
        )

        receipt = {
            "receipt_id": data["IDZ"],
            "date": pd.to_datetime(header_data["date"]),
            "store": "biedronka"
        }

        items = []
        current_item = None

        for entry in data["body"]:

            if "sellLine" in entry:

                sl = entry["sellLine"]

                current_item = {
                    "receipt_id": receipt["receipt_id"],
                    "raw_name": clean_raw_name(sl["name"]),
                    "quantity": float(sl["quantity"].replace(",", ".")),
                    "unit_price": sl["price"] / 100,
                    "total_price": sl["total"] / 100,
                    "discount": 0
                }

                items.append(current_item)

            elif "discountLine" in entry and current_item is not None:

                current_item["discount"] += (
                    entry["discountLine"]["value"] / 100
                )

        for item in items:

            item["final_price"] = round(
                item["total_price"] - item["discount"],
                2
            )

        return receipt, items


    def load_json_files(path):

        all_receipts = []
        all_items = []

        for file_path in path.glob("*.json"):

            with open(file_path, "r", encoding="utf-8") as f:

                data = json.load(f)

            receipt, items = parse_receipt(data)

            all_receipts.append(receipt)
            all_items.extend(items)

        receipts_df = pd.DataFrame(all_receipts)
        items_df = pd.DataFrame(all_items)

        return receipts_df, items_df


    def load_to_duckdb(receipts_df, items_df):

        con = duckdb.connect(DB_PATH)

        con.register("receipts_temp", receipts_df)

        con.execute("""
        CREATE OR REPLACE TABLE bronze_receipts AS
        SELECT * FROM receipts_temp
        """)

        con.register("items_temp", items_df)

        con.execute("""
        CREATE OR REPLACE TABLE bronze_receipts_items AS
        SELECT * FROM items_temp
        """)

        return con


    receipts_df, items_df = load_json_files(DATA_PATH)

    print(f"Receipts: {len(receipts_df)}")
    print(f"Items: {len(items_df)}")