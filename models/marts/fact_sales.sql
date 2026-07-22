-- BigQuery SQL DDL: Fact Sales Mart (Partitioned & Clustered for High Performance)
CREATE OR REPLACE TABLE `cellphones-analytics-prod.marts_cellphones.fact_sales`
PARTITION BY transaction_date
CLUSTER BY store_id, product_id AS

SELECT
  t.transaction_id,
  t.transaction_date,
  t.store_id,
  t.product_id,
  p.product_sk, -- Join with SCD2 Dimension surrogate key at time of purchase
  t.quantity,
  t.unit_price,
  t.total_amount
FROM `cellphones-analytics-prod.stg_cellphones.stg_transactions` t
LEFT JOIN `cellphones-analytics-prod.int_cellphones.dim_products_scd2` p
  ON t.product_id = p.product_id
 AND t.transaction_date BETWEEN p.valid_from AND p.valid_to;
