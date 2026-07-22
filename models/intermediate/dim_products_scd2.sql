-- BigQuery SQL DDL & DML: Slowly Changing Dimension (SCD Type 2) for Products
-- Part 1 Assessment Requirement: SCD Type 2 Architecture

-- Step 1: Create Target SCD Type 2 Table Schema
CREATE TABLE IF NOT EXISTS `cellphones-analytics-prod.int_cellphones.dim_products_scd2` (
  product_sk STRING,           -- Surrogate Key: FARM_FINGERPRINT(CONCAT(product_id, valid_from))
  product_id STRING,           -- Natural Key
  product_name STRING,
  brand STRING,
  category STRING,
  base_price NUMERIC,
  valid_from DATE,             -- Effective start date of dimension record
  valid_to DATE,               -- Effective end date (9999-12-31 if current)
  is_current BOOLEAN           -- TRUE if active version, FALSE if historical
);

-- Step 2: MERGE Statement to execute SCD Type 2 Update & Insert Pattern
MERGE `cellphones-analytics-prod.int_cellphones.dim_products_scd2` T
USING (
  -- Source Data with hash fingerprint of tracked attributes
  SELECT
    product_id,
    product_name,
    brand,
    category,
    base_price,
    CURRENT_DATE('Asia/Ho_Chi_Minh') AS effective_date,
    FARM_FINGERPRINT(CONCAT(COALESCE(product_name, ''), COALESCE(brand, ''), COALESCE(category, ''), CAST(base_price AS STRING))) AS attr_hash
  FROM `cellphones-analytics-prod.stg_cellphones.stg_products`
) S
ON T.product_id = S.product_id AND T.is_current = TRUE

-- 1. Expire existing active record if price or attributes changed
WHEN MATCHED AND (
  T.base_price != S.base_price OR 
  T.product_name != S.product_name OR 
  T.brand != S.brand OR 
  T.category != S.category
) THEN
  UPDATE SET 
    valid_to = S.effective_date - 1,
    is_current = FALSE

-- 2. Insert new product record if not existing in dimension table
WHEN NOT MATCHED THEN
  INSERT (
    product_sk,
    product_id,
    product_name,
    brand,
    category,
    base_price,
    valid_from,
    valid_to,
    is_current
  )
  VALUES (
    CAST(FARM_FINGERPRINT(CONCAT(S.product_id, '_', CAST(S.effective_date AS STRING))) AS STRING),
    S.product_id,
    S.product_name,
    S.brand,
    S.category,
    S.base_price,
    S.effective_date,
    DATE('9999-12-31'),
    TRUE
  );

-- Step 3: Insert the NEW active version for products whose attributes changed
INSERT INTO `cellphones-analytics-prod.int_cellphones.dim_products_scd2` (
  product_sk, product_id, product_name, brand, category, base_price, valid_from, valid_to, is_current
)
SELECT
  CAST(FARM_FINGERPRINT(CONCAT(S.product_id, '_', CAST(CURRENT_DATE('Asia/Ho_Chi_Minh') AS STRING))) AS STRING),
  S.product_id,
  S.product_name,
  S.brand,
  S.category,
  S.base_price,
  CURRENT_DATE('Asia/Ho_Chi_Minh'),
  DATE('9999-12-31'),
  TRUE
FROM `cellphones-analytics-prod.stg_cellphones.stg_products` S
JOIN `cellphones-analytics-prod.int_cellphones.dim_products_scd2` T
  ON S.product_id = T.product_id
WHERE T.is_current = FALSE AND T.valid_to = CURRENT_DATE('Asia/Ho_Chi_Minh') - 1;
