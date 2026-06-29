CREATE OR REPLACE VIEW gold_monthly_spending AS

WITH receipt_totals AS (

    SELECT
        receipt_id,

        CAST(date AS DATE) AS receipt_date,

        SUM(final_price) AS receipt_total,
        SUM(discount) AS receipt_discount,
        COUNT(*) AS item_count

    FROM silver_receipt_items
    WHERE is_food = true

    GROUP BY receipt_id, CAST(date AS DATE)

)

SELECT
    DATE_TRUNC('month', receipt_date)::DATE AS month_start,

    COUNT(receipt_id) AS receipt_count,

    ROUND(SUM(receipt_total), 2) AS total_spent,

    ROUND(SUM(receipt_discount), 2) AS total_discount,

    ROUND(
        SUM(receipt_discount)
        / NULLIF(SUM(receipt_total + receipt_discount), 0),
        3
    ) AS discount_ratio,

    SUM(item_count) AS items_bought,

    ROUND(MEDIAN(receipt_total), 2) AS median_receipt_value

FROM receipt_totals

GROUP BY 1
ORDER BY 1;