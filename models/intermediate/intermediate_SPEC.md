# Đặc tả Kỹ thuật Tầng Intermediate (SPEC)

## 1. Tổng quan
Lớp Intermediate (`int_cellphones`) thực hiện biến đổi dữ liệu phức tạp (Complex Transformations), bao gồm thiết kế **Slowly Changing Dimension Type 2 (SCD Type 2)** cho danh mục sản phẩm và tính toán cửa sổ trượt (Window Function - Moving Average 30d) cho chỉ số Daily Run Rate.

## 2. Đặc tả Thành phần Kỹ thuật

### 2.1 `dim_products_scd2` (Kiến trúc SCD Type 2)
- **Surrogate Key (`product_sk`)**: `FARM_FINGERPRINT(CONCAT(product_id, '_', valid_from))`
- **Các trường theo dõi**: `product_name`, `brand`, `category`, `base_price`.
- **Các trường thời gian**: `valid_from` (DATE), `valid_to` (DATE - Mặc định '9999-12-31'), `is_current` (BOOLEAN).
- **Mẫu thực thi**: Sử dụng kết hợp lệnh SQL `MERGE` và `INSERT INTO` để đóng bản ghi cũ (`valid_to = CURRENT_DATE - 1`, `is_current = FALSE`) và chèn phiên bản giá mới.

### 2.2 `int_daily_inventory_sales`
- **Chỉ số tính toán - Daily Run Rate**:
  ```sql
  AVG(sold_quantity) OVER (
    PARTITION BY store_id, product_id
    ORDER BY log_date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  )
  ```
- **Chỉ số tính toán - Inventory to Sales Ratio**:
  $$\text{Inventory\_to\_Sales\_Ratio} = \frac{\text{Ending\_Inventory}}{\text{Daily\_Run\_Rate}}$$
