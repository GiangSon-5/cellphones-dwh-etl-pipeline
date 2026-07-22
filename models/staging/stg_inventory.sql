-- BigQuery SQL DDL: Staging Inventory Logs View
CREATE OR REPLACE VIEW `cellphones-analytics-prod.stg_cellphones.stg_inventory` AS
SELECT
  PARSE_DATE('%Y-%m-%d', CAST(Log_Date AS STRING)) AS log_date,
  CAST(Store_ID AS STRING) AS store_id,
  CAST(Product_ID AS STRING) AS product_id,
  COALESCE(CAST(Beginning_Inventory AS INT64), 0) AS beginning_inventory,
  COALESCE(CAST(Received AS INT64), 0) AS received_quantity,
  COALESCE(CAST(Sold AS INT64), 0) AS sold_quantity,
  COALESCE(
    CAST(Ending_Inventory AS INT64), 
    COALESCE(CAST(Beginning_Inventory AS INT64), 0) + COALESCE(CAST(Received AS INT64), 0) - COALESCE(CAST(Sold AS INT64), 0)
  ) AS ending_inventory
FROM
  `cellphones-analytics-prod.raw_cellphones.inventory_logs`
WHERE
  Log_Date IS NOT NULL;
