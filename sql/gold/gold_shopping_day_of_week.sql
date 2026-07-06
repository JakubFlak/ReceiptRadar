CREATE OR REPLACE VIEW gold_shopping_day_of_week AS

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
    ((EXTRACT(DOW FROM date) + 6) % 7) AS weekday_order,
    
    DAYNAME(date) AS day_of_week,

    store,

    COUNT(*) AS receipt_count,

    ROUND(SUM(receipt_total), 2) AS total_spent,

    ROUND(AVG(receipt_total), 2) AS avg_receipt_value

FROM receipt_totals

GROUP BY
    weekday_order,
    day_of_week,
    store

ORDER BY
    weekday_order,
    store;