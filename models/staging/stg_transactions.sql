-- BigQuery SQL DDL: Staging Transactions View
CREATE OR REPLACE VIEW `cellphones-analytics-prod.stg_cellphones.stg_transactions` AS
SELECT
  CAST(Transaction_ID AS STRING) AS transaction_id,
  PARSE_DATE('%Y-%m-%d', CAST(Date AS STRING)) AS transaction_date,
  CAST(Product_ID AS STRING) AS product_id,
  CAST(Store_ID AS STRING) AS store_id,
  CAST(Quantity AS INT64) AS quantity,
  CAST(Unit_Price AS NUMERIC) AS unit_price,
  CAST(Quantity AS NUMERIC) * CAST(Unit_Price AS NUMERIC) AS total_amount
FROM
  `cellphones-analytics-prod.raw_cellphones.transactions`
WHERE
  Transaction_ID IS NOT NULL;
