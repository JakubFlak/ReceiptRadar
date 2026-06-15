CREATE OR REPLACE VIEW gold_shopping_day_of_week AS

WITH receipt_totals AS (

    SELECT
        receipt_id,
        date,
        SUM(final_price) AS receipt_total

    FROM silver_receipt_items

    GROUP BY
        receipt_id,
        date

)

SELECT
    DAYNAME(date) AS day_of_week,

    COUNT(*) AS receipt_count,

    ROUND(SUM(receipt_total), 2) AS total_spent,

    ROUND(AVG(receipt_total), 2) AS avg_receipt_value

FROM receipt_totals

GROUP BY day_of_week

ORDER BY total_spent DESC;