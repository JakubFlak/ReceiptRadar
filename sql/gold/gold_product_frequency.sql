CREATE OR REPLACE VIEW gold_product_frequency AS

WITH product_weeks AS (

    SELECT DISTINCT
        clean_name,
        DATE_TRUNC('week', date) AS week_start

    FROM silver_receipt_items

),

total_weeks AS (

    SELECT COUNT(DISTINCT DATE_TRUNC('week', date)) AS total_weeks
    FROM silver_receipt_items

)

SELECT
    pw.clean_name,

    COUNT(*) AS weeks_present,

    tw.total_weeks,

    ROUND(
        COUNT(*) * 100.0 / tw.total_weeks,
        1
    ) AS weekly_presence_pct

FROM product_weeks pw

CROSS JOIN total_weeks tw

GROUP BY
    pw.clean_name,
    tw.total_weeks

ORDER BY
    weekly_presence_pct DESC,
    weeks_present DESC;