-- BigQuery SQL DDL: Mart Sales Performance Aggregation (Store vs Target)
CREATE OR REPLACE TABLE `cellphones-analytics-prod.marts_cellphones.marts_sales_performance` AS
WITH monthly_sales AS (
  SELECT
    store_id,
    FORMAT_DATE('%Y-%m', transaction_date) AS month_year,
    SUM(total_amount) AS actual_revenue,
    SUM(quantity) AS total_units_sold,
    COUNT(DISTINCT transaction_id) AS total_orders
  FROM `cellphones-analytics-prod.marts_cellphones.fact_sales`
  GROUP BY 1, 2
)

SELECT
  s.store_id,
  st.store_name,
  st.region,
  st.store_type,
  s.month_year,
  s.actual_revenue,
  COALESCE(t.target_revenue, 0) AS target_revenue,
  SAFE_DIVIDE(s.actual_revenue, t.target_revenue) AS achievement_pct,
  CASE
    WHEN SAFE_DIVIDE(s.actual_revenue, t.target_revenue) >= 1.10 THEN 'Super Star (>=110%)'
    WHEN SAFE_DIVIDE(s.actual_revenue, t.target_revenue) >= 0.90 THEN 'On Track (90-109%)'
    WHEN SAFE_DIVIDE(s.actual_revenue, t.target_revenue) >= 0.70 THEN 'Underperforming (70-89%)'
    ELSE 'Critical Warning (<70%)'
  END AS performance_status
FROM monthly_sales s
LEFT JOIN `cellphones-analytics-prod.stg_cellphones.stg_stores` st ON s.store_id = st.store_id
LEFT JOIN `cellphones-analytics-prod.stg_cellphones.stg_targets` t ON s.store_id = t.store_id AND s.month_year = t.month_year;
