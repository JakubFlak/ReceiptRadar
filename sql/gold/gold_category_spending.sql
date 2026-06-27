CREATE OR REPLACE VIEW gold_category_spending AS

SELECT
    DATE_TRUNC('month', date) AS month_start,
    category,
    subcategory,

    COUNT(*) AS items_bought,

    ROUND(SUM(quantity), 2) AS total_quantity,

    ROUND(SUM(final_price), 2) AS total_spent,

    ROUND(SUM(discount), 2) AS total_discount

FROM silver_receipt_items

WHERE is_food = true

GROUP BY
    1,
    2,
    3

ORDER BY
    month_start,
    total_spent DESC;