-- BigQuery SQL DDL: Dimension Store Mart
CREATE OR REPLACE TABLE `cellphones-analytics-prod.marts_cellphones.dim_store` AS
SELECT
  store_id,
  store_name,
  region,
  regional_sales_manager,
  area_manager,
  store_type,
  CASE
    WHEN store_type = 'A' THEN 'Flagship Store'
    WHEN store_type = 'B' THEN 'Key Store'
    WHEN store_type = 'C' THEN 'Standard Store'
    ELSE 'Micro Store'
  END AS store_tier
FROM `cellphones-analytics-prod.stg_cellphones.stg_stores`;
