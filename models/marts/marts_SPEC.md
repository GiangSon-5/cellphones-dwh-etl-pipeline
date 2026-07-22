# Đặc tả Kỹ thuật Tầng Marts (SPEC)

## 1. Tổng quan
Lớp Marts (`marts_cellphones`) thiết kế theo mô hình Star Schema chuẩn gồm các bảng Dimension (`dim_store`, `dim_product`) và bảng Fact (`fact_sales`, `fact_inventory_daily`, `marts_sales_performance`).

## 2. Chiến lược Tối ưu BigQuery Partition & Cluster
- `fact_sales`: Partition theo `transaction_date` (DAY), Cluster theo `store_id`, `product_id`.
- `fact_inventory_daily`: Partition theo `log_date` (DAY), Cluster theo `store_id`, `product_id`.
- Mục đích: Giảm tối đa dung lượng dữ liệu quét (Bytes Scanned) khi Power BI query theo vùng miền, ngày giao dịch hoặc mã cửa hàng.
