CREATE OR REPLACE VIEW gold_discount_analysis AS

SELECT
    DATE_TRUNC('month', date) AS month_start,

    ROUND(SUM(total_price), 2) AS gross_spend,

    ROUND(SUM(discount), 2) AS total_discount,

    ROUND(SUM(final_price), 2) AS net_spend,

    ROUND(
        SUM(discount)
        * 100.0
        / NULLIF(SUM(total_price), 0),
        2
    ) AS discount_pct

FROM silver_receipt_items

WHERE is_food = true

GROUP BY 1

ORDER BY month_start;