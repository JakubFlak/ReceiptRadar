CREATE OR REPLACE VIEW silver_receipt_items AS

SELECT
    bri.receipt_id,
    br.date,
    br.store,

    bri.raw_name,
    dp.clean_name,
    dp.category,
    dp.subcategory,

    bri.quantity,
    bri.unit_price,
    bri.total_price,
    bri.discount,
    bri.final_price

FROM bronze_receipts_items bri

LEFT JOIN bronze_receipts br
    ON bri.receipt_id = br.receipt_id

LEFT JOIN dim_products dp
    ON bri.raw_name = dp.raw_name
    AND br.store = dp.store