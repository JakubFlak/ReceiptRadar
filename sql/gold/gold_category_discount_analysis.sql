CREATE OR REPLACE VIEW gold_category_discount_analysis AS

SELECT
    category,
    subcategory,

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

GROUP BY
    category,
    subcategory

ORDER BY total_discount DESC;