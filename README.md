# ReceiptRadar



[![Python tests](https://github.com/JakubFlak/ReceiptRadar/actions/workflows/python-tests.yml/badge.svg)](https://github.com/JakubFlak/ReceiptRadar/actions/workflows/python-tests.yml)

<!-- BADGES_START -->
![receipts](https://img.shields.io/badge/receipts-48-blue)
![products](https://img.shields.io/badge/products-1142-green)
![stores](https://img.shields.io/badge/stores-2-purple)
![data_freshness](https://img.shields.io/badge/data_freshness-2026.06.24-orange)
<!-- BADGES_END -->


> For a business-focused project summary covering analytical goals, key questions, architecture, metrics, and insights, see `README_BUSINESS.md`.

# ReceiptRadar

ReceiptRadar is a receipt analytics pipeline that extracts supermarket receipt data from multiple store formats, normalizes product names, and builds analytical views in DuckDB.

## Why this project exists

The goal of ReceiptRadar is to turn raw receipt exports into a reusable analytics warehouse. It supports multiple receipt formats, maintains a product mapping layer, and generates silver/gold views for spending, category, store, and time-based analysis.

## What it does

- Parses raw receipt files from:
  - `Biedronka` JSON receipts
  - `Lidl` text receipts
- Loads receipts and line items into bronze tables in DuckDB
- Uses `data/mappings/products.csv` to normalize raw product names and generate stable product IDs
- Detects unmapped products and updates the mapping file automatically
- Builds silver/gold SQL views for analytics and reporting

## Pipeline flow

1. `src.warehouse.create_bronze_tables` creates the local DuckDB warehouse tables
2. `src.warehouse.run_bronze_ingestion` reads raw receipt files and loads them into bronze tables
3. `src.mappings.load_dim_products` loads the product mapping into `dim_products`
4. `src.mappings.find_unmapped_products` identifies unmapped items and updates the mapping CSV
5. `src.warehouse.run_silver_models` runs SQL in `sql/silver`
6. `src.warehouse.run_gold_models` runs SQL in `sql/gold`

## Analytical outputs

The repository is designed to support analytics from a receipt-centric warehouse, including:

- Receipt and item ingestion accuracy
- Raw product normalization via mapping and stable `product_id`
- Category- and store-level spend analysis
- Weekly and monthly spending trends
- Shopping time and day-of-week patterns
- Product frequency and discount analysis

## Project structure

- `data/`
  - `raw/` - raw receipt files from stores
  - `mappings/` - product mapping CSV and enrichment data
  - `warehouse/` - DuckDB warehouse file
- `src/`
  - `mappings/` - mapping loader and unmapped-product detection
  - `parsers/` - parser implementations for each store
  - `pipeline/` - pipeline entrypoint
  - `warehouse/` - DuckDB table creation and model execution
- `sql/`
  - `silver/` - silver layer view definitions
  - `gold/` - gold analytics view definitions
- `tests/` - unit and integration tests
- `notebooks/` - exploratory notebooks and experiments

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run the pipeline

From the project root:

```bash
python -m src.pipeline.run_pipeline
```

This will create the warehouse, ingest raw receipts, apply product mapping, and materialize silver/gold views.

## Run tests

Execute the automated test suite with:

```bash
pytest
```

## Data sources

- `data/raw/biedronka/json/` contains Biedronka receipt JSON exports
- `data/raw/lidl/` contains Lidl receipt text exports
- `data/mappings/products.csv` is the canonical product mapping file used to normalize raw item names and assign product IDs

## Notes

- DuckDB is used for local warehouse storage at `data/warehouse/warehouse.db`
- The pipeline is idempotent for bronze ingestion: it avoids duplicate receipts and items when rerun
- Unmapped raw products are detected and appended to `data/mappings/products.csv`, making the mapping file the main source of truth

## Useful commands

- `python -m src.pipeline.run_pipeline` - run the full pipeline
- `pytest` - run tests
- `pip install -r requirements.txt` - install dependencies
