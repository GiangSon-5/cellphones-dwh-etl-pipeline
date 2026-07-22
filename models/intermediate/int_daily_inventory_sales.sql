-- BigQuery SQL DDL: Intermediate Daily Inventory & Sales Aggregation with Metrics
CREATE OR REPLACE TABLE `cellphones-analytics-prod.int_cellphones.int_daily_inventory_sales`
PARTITION BY log_date
CLUSTER BY store_id, product_id AS

WITH daily_sales AS (
  SELECT
    transaction_date AS log_date,
    store_id,
    product_id,
    SUM(quantity) AS daily_sales_qty,
    SUM(total_amount) AS daily_sales_amount
  FROM `cellphones-analytics-prod.stg_cellphones.stg_transactions`
  GROUP BY 1, 2, 3
),

inventory_with_sales AS (
  SELECT
    inv.log_date,
    inv.store_id,
    inv.product_id,
    inv.beginning_inventory,
    inv.received_quantity,
    COALESCE(s.daily_sales_qty, inv.sold_quantity, 0) AS sold_quantity,
    inv.ending_inventory,
    COALESCE(s.daily_sales_amount, 0) AS daily_sales_amount
  FROM `cellphones-analytics-prod.stg_cellphones.stg_inventory` inv
  LEFT JOIN daily_sales s
    ON inv.log_date = s.log_date
   AND inv.store_id = s.store_id
   AND inv.product_id = s.product_id
),

-- Calculate 30-Day Moving Average Daily Run Rate (DRR)
drr_calculated AS (
  SELECT
    *,
    AVG(sold_quantity) OVER (
      PARTITION BY store_id, product_id
      ORDER BY log_date
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS daily_run_rate_30d
  FROM inventory_with_sales
)

SELECT
  log_date,
  store_id,
  product_id,
  beginning_inventory,
  received_quantity,
  sold_quantity,
  ending_inventory,
  daily_sales_amount,
  ROUND(daily_run_rate_30d, 2) AS daily_run_rate,
  CASE
    WHEN daily_run_rate_30d > 0 THEN ROUND(ending_inventory / daily_run_rate_30d, 2)
    ELSE 999.0
  END AS inventory_to_sales_ratio,
  CASE
    WHEN daily_run_rate_30d > 0 AND (ending_inventory / daily_run_rate_30d) <= 2.0 THEN 'CRITICAL STOCKOUT RISK'
    WHEN daily_run_rate_30d > 0 AND (ending_inventory / daily_run_rate_30d) <= 5.0 THEN 'LOW INVENTORY WARNING'
    WHEN daily_run_rate_30d > 0 AND (ending_inventory / daily_run_rate_30d) <= 15.0 THEN 'OPTIMAL STOCK'
    ELSE 'OVERSTOCK RISK'
  END AS inventory_health_status
FROM drr_calculated;
