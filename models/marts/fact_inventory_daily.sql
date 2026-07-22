-- BigQuery SQL DDL: Fact Inventory Daily Mart (Partitioned & Clustered)
CREATE OR REPLACE TABLE `cellphones-analytics-prod.marts_cellphones.fact_inventory_daily`
PARTITION BY log_date
CLUSTER BY store_id, product_id AS

SELECT
  log_date,
  store_id,
  product_id,
  beginning_inventory,
  received_quantity,
  sold_quantity,
  ending_inventory,
  daily_sales_amount,
  daily_run_rate,
  inventory_to_sales_ratio,
  inventory_health_status
FROM `cellphones-analytics-prod.int_cellphones.int_daily_inventory_sales`;
