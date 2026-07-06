CREATE OR REPLACE VIEW gold_dim_store AS

SELECT DISTINCT
    store
FROM silver_receipt_items;