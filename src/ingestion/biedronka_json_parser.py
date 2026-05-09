import os
import json
import pandas as pd

DATA_PATH = "data/raw/biedronka/json"

def load_json_files(path):
    all_receipts = []
    all_items = []

    for filename in os.listdir(path):
        if filename.endswith(".json"):
            file_path = os.path.join(path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            receipt, items = parse_receipt(data)

            all_receipts.append(receipt)
            all_items.extend(items)
            
            receipts_df = pd.DataFrame(all_receipts)
            items_df = pd.DataFrame(all_items)

    return receipts_df, items_df

def parse_receipt(data):
    header_data = next(
        h["headerData"] for h in data["header"] if "headerData" in h
    )

    receipt = {
        "receipt_id": data["IDZ"],
        "date": header_data["date"],
        "store": "biedronka"
    }

    items = []
    current_item = None

    for entry in data["body"]:
        if "sellLine" in entry:
            sl = entry["sellLine"]

            current_item = {
                "receipt_id": receipt["receipt_id"],
                "name": sl["name"].strip().rsplit(" ", 1)[0],
                "quantity": float(sl["quantity"].replace(",", ".")),
                "unit_price": sl["price"] / 100,
                "total_price": sl["total"] / 100,
                "discount": 0,
            }

            items.append(current_item)

        elif "discountLine" in entry and current_item is not None:
            current_item["discount"] += (
                entry["discountLine"]["value"] / 100
            )
            
    for item in items:
        item["final_price"] = round(item["total_price"] - item["discount"], 2)

    return receipt, items

receipts_df, items_df = load_json_files(DATA_PATH)
print(receipts_df.shape)
print(receipts_df.head())

print(items_df.shape)
print(items_df.head())

import duckdb

con = duckdb.connect("data/warehouse.db")

con.register("receipts_temp", receipts_df)

con.execute("""
CREATE OR REPLACE TABLE receipts AS
SELECT * FROM receipts_temp
""")

con.register("items_temp", items_df)

con.execute("""
CREATE OR REPLACE TABLE receipts_items AS
SELECT * FROM items_temp
""")

print(con.execute("""
SELECT
    r.date,
    r.store,
    SUM(i.final_price) as receipt_total
FROM receipts r
JOIN receipts_items i
    ON r.receipt_id = i.receipt_id
GROUP BY r.receipt_id, r.date, r.store
ORDER BY receipt_total DESC
""").fetchdf())