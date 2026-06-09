from src.ingestion.biedronka_json_parser import load_biedronka
from src.mappings.load_dim_products import load_dim_products
from src.warehouse.run_silver_models import run_silver_models
from src.warehouse.run_gold_models import run_gold_models

def run_pipeline():

    print("Loading raw receipts...")
    load_biedronka()

    print("Loading product mapping...")
    load_dim_products()

    print("Building silver layer...")
    run_silver_models()

    print("Building gold layer...")
    run_gold_models()

    print("Pipeline completed")


if __name__ == "__main__":
    run_pipeline()