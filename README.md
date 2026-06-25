# ReceiptRadar

[![Python tests](https://github.com/<your-username>/<your-repo>/actions/workflows/python-tests.yml/badge.svg)](https://github.com/<your-username>/<your-repo>/actions/workflows/python-tests.yml)

ReceiptRadar is a small data pipeline project for processing supermarket receipts from multiple stores and building analytical views from them.

## What it does

- Parses receipt data from raw files for Biedronka and Lidl
- Loads parsed receipts into a bronze layer in DuckDB
- Maps raw product names to normalized product dimensions
- Builds silver and gold analytics views for spending and product analysis

## Project structure

- data/ - raw receipts and product mapping data
- src/ - Python pipeline code
  - mappings/ - product mapping and unmapped-product detection
  - parsers/ - receipt parsers for each store
  - pipeline/ - pipeline entrypoint
  - warehouse/ - bronze table setup and ingestion logic
- sql/ - SQL definitions for silver and gold views
- notebooks/ - exploratory notebooks

## Requirements

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

## Run the pipeline

From the project root, run:

```bash
python -m src.pipeline.run_pipeline
```

This will:

1. Create the bronze tables
2. Load raw receipt data
3. Load the product mapping table
4. Detect unmapped products
5. Build silver and gold views

## Notes

- The mapping file at data/mappings/products.csv is the main place to normalize product names and categories.
- The pipeline currently uses DuckDB for local warehouse storage.
