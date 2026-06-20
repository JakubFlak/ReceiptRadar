from src.ingestion.biedronka_json_parser import load_biedronka
from src.mappings.load_dim_products import load_dim_products
from src.mappings.find_unmapped_products import find_unmapped_products
from src.warehouse.run_silver_models import run_silver_models
from src.warehouse.run_gold_models import run_gold_models
from src.warehouse.create_bronze_tables import create_bronze_tables

def run_pipeline():

    print("\nCreating bronze tables...")
    create_bronze_tables()

    print("\nLoading raw receipts...")
    load_biedronka()

    print("\nLoading product mapping...")
    load_dim_products()

    print("\nAnalyzing unmapped products...")
    find_unmapped_products()

    print("\nBuilding silver layer...")
    run_silver_models()

    print("\nBuilding gold layer...")
    run_gold_models()

    print("\nPipeline completed")


if __name__ == "__main__":
    run_pipeline()