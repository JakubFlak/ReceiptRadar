from pathlib import Path
import pandas as pd
import re


def load_lidl():

    DATA_PATH = Path(
        "data/raw/lidl"
    )

    for file_path in DATA_PATH.glob("*.txt"):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        receipt, items = parse_receipt(
            text,
            file_path.stem
        )

        print(receipt)


def parse_receipt(
    text: str,
    file_name: str
):

    lines = [
        line.rstrip()
        for line in text.splitlines()
        if line.strip()
    ]

    date = None

    for line in lines:

        if re.match(
            r"\d{4}-\d{2}-\d{2}",
            line
        ):
            date = pd.to_datetime(line)
            break

    receipt_number = None
    receipt_time = None

    for line in lines:

        match = re.search(
            r"nr:\s*(\d+)\s+(\d{2}:\d{2})",
            line
        )

        if match:
            receipt_number = match.group(1)
            receipt_time = match.group(2)
            break
    
    receipt_datetime = pd.to_datetime(
        f"{date.date()} {receipt_time}"
    )

    receipt = {
        "receipt_id": f"lidl_{file_name}_{receipt_number}",
        "date": receipt_datetime,
        "store": "lidl"
    }

    items = []

    for i in range(len(lines) - 1):

        product_name = lines[i].strip()
        details_line = lines[i + 1].strip()

        print(product_name)
        print(details_line)
        print("---")

    return receipt, items


if __name__ == "__main__":
    load_lidl()