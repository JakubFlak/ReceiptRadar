CREATE OR REPLACE VIEW gold_shopping_time_of_day AS

WITH receipt_totals AS (
    SELECT
        receipt_id,
        date,
        store,
        SUM(final_price) AS receipt_total
    FROM silver_receipt_items
    WHERE is_food = true
    GROUP BY
        receipt_id,
        date,
        store
)

SELECT
    CASE
        WHEN EXTRACT(hour FROM date) BETWEEN 5 AND 10 THEN 1
        WHEN EXTRACT(hour FROM date) BETWEEN 11 AND 15 THEN 2
        WHEN EXTRACT(hour FROM date) BETWEEN 16 AND 20 THEN 3
        ELSE 4
    END AS time_of_day_order,
    CASE
        WHEN EXTRACT(hour FROM date) BETWEEN 5 AND 10 THEN 'Morning'
        WHEN EXTRACT(hour FROM date) BETWEEN 11 AND 15 THEN 'Afternoon'
        WHEN EXTRACT(hour FROM date) BETWEEN 16 AND 20 THEN 'Evening'
        ELSE 'Night'
    END AS time_of_day,
    store,
    COUNT(*) AS receipt_count,
    ROUND(SUM(receipt_total), 2) AS total_spent,
    ROUND(AVG(receipt_total), 2) AS avg_receipt_value
FROM receipt_totals
GROUP BY
    time_of_day_order,
    time_of_day,
    store
ORDER BY
    time_of_day_order,
    store;