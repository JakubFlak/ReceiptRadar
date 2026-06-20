from pathlib import Path
import pandas as pd
import re


# ==========================
# PUBLIC API (USED BY PIPELINE)
# ==========================
def parse_lidl_files(path: Path):

    all_receipts = []
    all_items = []

    for file_path in path.glob("*.txt"):

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        receipt, items = parse_receipt(text, file_path.stem)

        all_receipts.append(receipt)
        all_items.extend(items)

    return all_receipts, all_items


# ==========================
# CORE PARSER
# ==========================
def parse_receipt(text: str, file_name: str):

    lines = [
        line.rstrip()
        for line in text.splitlines()
        if line.strip()
    ]

    # --------------------------
    # DATE
    # --------------------------
    date = None

    for line in lines:
        if re.match(r"\d{4}-\d{2}-\d{2}", line):
            date = pd.to_datetime(line)
            break

    # --------------------------
    # RECEIPT META
    # --------------------------
    receipt_number = None
    receipt_time = None

    for line in lines:
        match = re.search(r"nr:\s*(\d+)\s+(\d{2}:\d{2})", line)
        if match:
            receipt_number = match.group(1)
            receipt_time = match.group(2)
            break

    receipt_datetime = pd.to_datetime(f"{date.date()} {receipt_time}")

    receipt = {
        "receipt_id": f"lidl_{file_name}_{receipt_number}",
        "date": receipt_datetime,
        "store": "lidl"
    }

    # --------------------------
    # ITEMS
    # --------------------------
    items = []
    current_item = None

    for i in range(len(lines) - 1):

        product_name = lines[i].strip()
        details_line = lines[i + 1].strip()

        # UNIT PRODUCTS
        unit_match = re.match(
            r"(\d+)\s+\*\s+([\d.]+)\s+([\d.]+)",
            details_line
        )

        if unit_match:
            current_item = {
                "receipt_id": receipt["receipt_id"],
                "raw_name": product_name,
                "quantity": float(unit_match.group(1)),
                "unit_price": float(unit_match.group(2)),
                "total_price": float(unit_match.group(3)),
                "discount": 0.0
            }
            items.append(current_item)
            continue

        # WEIGHT PRODUCTS
        weight_match = re.match(
            r"([\d,]+)kg\s+x\s+([\d.]+)\s+([\d.]+)",
            details_line
        )

        if weight_match:
            current_item = {
                "receipt_id": receipt["receipt_id"],
                "raw_name": product_name,
                "quantity": float(weight_match.group(1).replace(",", ".")),
                "unit_price": float(weight_match.group(2)),
                "total_price": float(weight_match.group(3)),
                "discount": 0.0
            }
            items.append(current_item)
            continue

        # DISCOUNTS
        discount_match = re.search(r"-(\d+,\d+)", product_name)

        if discount_match and current_item is not None:
            current_item["discount"] += float(
                discount_match.group(1).replace(",", ".")
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