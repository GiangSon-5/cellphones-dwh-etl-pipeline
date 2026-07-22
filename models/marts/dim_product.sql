-- BigQuery SQL DDL: Dimension Product Mart (Current Active Version)
CREATE OR REPLACE TABLE `cellphones-analytics-prod.marts_cellphones.dim_product` AS
SELECT
  product_sk,
  product_id,
  product_name,
  brand,
  category,
  base_price,
  valid_from,
  valid_to,
  is_current
FROM `cellphones-analytics-prod.int_cellphones.dim_products_scd2`
WHERE is_current = TRUE;
