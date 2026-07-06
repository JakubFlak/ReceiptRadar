CREATE OR REPLACE VIEW gold_receipts_histogram AS

SELECT
	bri.receipt_id,
	br.store,
	SUM(bri.final_price) AS total_receipt_price
FROM bronze_receipts_items bri
JOIN bronze_receipts br ON br.receipt_id = bri.receipt_id
GROUP BY bri.receipt_id, br.store
ORDER BY SUM(bri.final_price) DESC
