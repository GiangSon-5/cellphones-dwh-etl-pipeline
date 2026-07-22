-- BigQuery SQL DDL: Staging Products View
CREATE OR REPLACE VIEW `cellphones-analytics-prod.stg_cellphones.stg_products` AS
SELECT
  CAST(Product_ID AS STRING) AS product_id,
  CAST(Product_Name AS STRING) AS product_name,
  CAST(Brand AS STRING) AS brand,
  CAST(Category AS STRING) AS category,
  CAST(Base_Price AS NUMERIC) AS base_price
FROM
  `cellphones-analytics-prod.raw_cellphones.products`
WHERE
  Product_ID IS NOT NULL;
