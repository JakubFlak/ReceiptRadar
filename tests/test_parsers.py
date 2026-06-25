import json
from pathlib import Path

from src.parsers.biedronka_json_parser import parse_biedronka_files
from src.parsers.lidl_txt_parser import parse_lidl_files


def test_parse_biedronka_files_returns_receipts_and_items(tmp_path):
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(
        json.dumps(
            {
                "IDZ": "r001",
                "header": [{"headerData": {"date": "2024-01-01"}}],
                "body": [
                    {
                        "sellLine": {
                            "name": "Milk 2l",
                            "quantity": "1,0",
                            "price": 250,
                            "total": 250,
                        }
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    receipts, items = parse_biedronka_files(tmp_path)

    assert len(receipts) == 1
    assert receipts[0]["receipt_id"] == "r001"
    assert receipts[0]["store"] == "biedronka"
    assert len(items) == 1
    assert items[0]["raw_name"] == "Milk"
    assert items[0]["quantity"] == 1.0
    assert items[0]["final_price"] == 2.5


def test_parse_lidl_files_returns_receipts_and_items(tmp_path):
    receipt_path = tmp_path / "receipt.txt"
    receipt_path.write_text(
        "2024-01-02\n"
        "Some shop\n"
        "nr: 123 10:30\n"
        "Bread\n"
        "2 * 1.50 3.00\n",
        encoding="utf-8",
    )

    receipts, items = parse_lidl_files(tmp_path)

    assert len(receipts) == 1
    assert receipts[0]["receipt_id"] == "lidl_receipt_123"
    assert receipts[0]["store"] == "lidl"
    assert len(items) == 1
    assert items[0]["raw_name"] == "Bread"
    assert items[0]["quantity"] == 2.0
    assert items[0]["unit_price"] == 1.5
    assert items[0]["final_price"] == 3.0
