/*
monthly/week spending 
category and subcategory spending (could be done later on in power bi with a slicer) 
discount analysis (maybe how much i save on each shopping/monthly/how much it reduces the price in percentage per shopping)/discounts in total (as a KPI) 
basket composition but mainly to get products that are almost evey time bought (but it should be checked for the week period) 
shopping habits (days for shopping, typical hour ranges) 
percentage or some broader analysis on healthy/junk food that i buy and consume
*/


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