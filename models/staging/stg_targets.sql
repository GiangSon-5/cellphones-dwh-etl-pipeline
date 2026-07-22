-- BigQuery SQL DDL: Staging Targets View
CREATE OR REPLACE VIEW `cellphones-analytics-prod.stg_cellphones.stg_targets` AS
SELECT
  CAST(Store_ID AS STRING) AS store_id,
  CAST(Month_Year AS STRING) AS month_year,
  CAST(Target_Revenue AS NUMERIC) AS target_revenue
FROM
  `cellphones-analytics-prod.raw_cellphones.targets`
WHERE
  Store_ID IS NOT NULL AND Month_Year IS NOT NULL;
