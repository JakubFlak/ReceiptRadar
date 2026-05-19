CREATE OR REPLACE VIEW gold_category_spending AS

SELECT
    category,

    ROUND(SUM(final_price), 2) AS total_spent,
    COUNT(*) AS items_bought,
    ROUND(AVG(final_price), 2) AS avg_item_price

FROM silver_receipt_items

GROUP BY
    category

ORDER BY total_spent DESC