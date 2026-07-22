-- BigQuery SQL DDL: Staging Store Info View
CREATE OR REPLACE VIEW `cellphones-analytics-prod.stg_cellphones.stg_stores` AS
SELECT
  CAST(Store_ID AS STRING) AS store_id,
  CAST(Store_Name AS STRING) AS store_name,
  CAST(Region AS STRING) AS region,
  CAST(RSM AS STRING) AS regional_sales_manager,
  CAST(AM AS STRING) AS area_manager,
  CAST(Store_Type AS STRING) AS store_type
FROM
  `cellphones-analytics-prod.raw_cellphones.store_info`
WHERE
  Store_ID IS NOT NULL;
