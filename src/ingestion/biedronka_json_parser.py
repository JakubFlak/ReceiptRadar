import os
import json
import pandas as pd

DATA_PATH = "data/raw/biedronka/json"

def load_json_files(path):
    all_items = []

    for filename in os.listdir(path):
        if filename.endswith(".json"):
            file_path = os.path.join(path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            items = parse_receipt(data)
            all_items.extend(items)

    return pd.DataFrame(all_items)

def parse_receipt(data):
    header_data = next(
        h["headerData"] for h in data["header"] if "headerData" in h
    )

    receipt_id = data["IDZ"]

    items = []
    current_item = None

    for entry in data["body"]:
        if "sellLine" in entry:
            sl = entry["sellLine"]

            current_item = {
                "name": sl["name"].strip().rsplit(" ", 1)[0],
                "quantity": float(sl["quantity"].replace(",", ".")),
                "unit_price": sl["price"] / 100,
                "total_price": sl["total"] / 100,
                "discount": 0,
                "receipt_id": receipt_id
            }

            items.append(current_item)

        elif "discountLine" in entry and current_item is not None:
            current_item["discount"] += entry["discountLine"]["value"] / 100

    for item in items:
        item["final_price"] = round(item["total_price"] - item["discount"], 2)

    return items

df = load_json_files(DATA_PATH)

print(df.shape)
print(df.head())

import duckdb

con = duckdb.connect("data/warehouse.duckdb")

con.register("df_temp", df)

con.execute("""
CREATE OR REPLACE TABLE receipts_items AS
SELECT * FROM df_temp
""")

print(con.execute("SELECT COUNT(*) FROM receipts_items").fetchall())

print(con.execute("""
SELECT name, SUM(final_price) as total_spent
FROM receipts_items
GROUP BY name
ORDER BY total_spent DESC
LIMIT 10
""").fetchdf())