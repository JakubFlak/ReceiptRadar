CREATE OR REPLACE VIEW gold_product_frequency AS

WITH product_weeks AS (

    SELECT DISTINCT
        clean_name,
        store,
        DATE_TRUNC('week', date) AS week_start

    FROM silver_receipt_items

    WHERE is_food = true

),

total_weeks AS (

    SELECT
        store,
        COUNT(DISTINCT DATE_TRUNC('week', date)) AS total_weeks

    FROM silver_receipt_items

    WHERE is_food = true

    GROUP BY store

)

SELECT
    pw.clean_name,

    pw.store,

    COUNT(*) AS weeks_present,

    tw.total_weeks,

    ROUND(
        COUNT(*) * 100.0 / tw.total_weeks,
        1
    ) AS weekly_presence_pct

FROM product_weeks pw

JOIN total_weeks tw
    ON pw.store = tw.store

GROUP BY
    pw.clean_name,
    pw.store,
    tw.total_weeks

ORDER BY
    pw.store,
    weekly_presence_pct DESC,
    weeks_present DESC;