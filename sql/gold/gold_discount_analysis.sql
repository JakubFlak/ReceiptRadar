CREATE OR REPLACE VIEW gold_discount_analysis AS

WITH base AS (
    SELECT
        receipt_id,
        CAST(date AS DATE) AS receipt_date,
        store,
        total_price,
        discount,
        final_price
    FROM silver_receipt_items
    WHERE is_food = true
)

SELECT
    DATE_TRUNC('month', receipt_date)::DATE AS month_start,
    store,
    ROUND(SUM(total_price), 2) AS gross_spend,
    ROUND(SUM(discount), 2) AS total_discount,
    ROUND(SUM(final_price), 2) AS net_spend,
    ROUND(
        SUM(discount)
        * 100.0
        / NULLIF(SUM(total_price), 0),
        2
    ) AS discount_pct
FROM base
GROUP BY
    1,
    2
ORDER BY
    1,
    2;