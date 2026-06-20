from pathlib import Path
import json
import pandas as pd
from src.utils.product_cleaning import clean_raw_name


# ==========================
# PUBLIC API
# ==========================
def parse_biedronka_files(path: Path):

    all_receipts = []
    all_items = []

    for file_path in path.glob("*.json"):

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        receipt, items = parse_receipt(data)

        all_receipts.append(receipt)
        all_items.extend(items)

    return all_receipts, all_items


# ==========================
# CORE PARSER
# ==========================
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

        # --------------------------
        # ITEM
        # --------------------------
        if "sellLine" in entry:

            sl = entry["sellLine"]

            current_item = {
                "receipt_id": receipt["receipt_id"],
                "raw_name": clean_raw_name(sl["name"]),
                "quantity": float(sl["quantity"].replace(",", ".")),
                "unit_price": sl["price"] / 100,
                "total_price": sl["total"] / 100,
                "discount": 0.0
            }

            items.append(current_item)

        # --------------------------
        # DISCOUNT
        # --------------------------
        elif "discountLine" in entry and current_item is not None:

            current_item["discount"] += (
                entry["discountLine"]["value"] / 100
            )

    # --------------------------
    # FINAL PRICE
    # --------------------------
    for item in items:
        item["final_price"] = round(
            item["total_price"] - item["discount"],
            2
        )

    return receipt, items