CREATE OR REPLACE VIEW gold_shopping_time_of_day AS

WITH receipt_totals AS (

    SELECT
        receipt_id,
        date,
        SUM(final_price) AS receipt_total

    FROM silver_receipt_items

    WHERE is_food = true

    GROUP BY
        receipt_id,
        date

)

SELECT
    CASE
        WHEN EXTRACT(hour FROM date) BETWEEN 5 AND 10
            THEN 'Morning'

        WHEN EXTRACT(hour FROM date) BETWEEN 11 AND 15
            THEN 'Afternoon'

        WHEN EXTRACT(hour FROM date) BETWEEN 16 AND 20
            THEN 'Evening'

        ELSE 'Night'
    END AS time_of_day,

    COUNT(*) AS receipt_count,

    ROUND(SUM(receipt_total), 2) AS total_spent,

    ROUND(AVG(receipt_total), 2) AS avg_receipt_value

FROM receipt_totals

GROUP BY time_of_day

ORDER BY receipt_count DESC;