CREATE OR REPLACE VIEW gold_category_spending AS

WITH base AS (
    SELECT
        CAST(date AS DATE) AS receipt_date,
        store,
        category,
        subcategory,
        quantity,
        final_price,
        discount
    FROM silver_receipt_items
    WHERE is_food = true
)

SELECT
    DATE_TRUNC('month', receipt_date)::DATE AS month_start,
    store,
    category,
    subcategory,
    COUNT(*) AS items_bought,
    ROUND(SUM(quantity), 2) AS total_quantity,
    ROUND(SUM(final_price), 2) AS total_spent,
    ROUND(SUM(discount), 2) AS total_discount
FROM base
GROUP BY
    1,
    2,
    3,
    4
ORDER BY
    month_start,
    store,
    total_spent DESC;