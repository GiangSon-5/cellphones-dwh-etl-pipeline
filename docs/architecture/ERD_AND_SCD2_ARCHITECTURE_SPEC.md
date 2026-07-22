# Đặc tả Kỹ thuật Kiến trúc & SCD Type 2 (SPEC)

## 1. Tổng quan Đặc tả
Tài liệu này quy định đặc tả kỹ thuật chi tiết cho mô hình dữ liệu Data Warehouse và chiến lược Slowly Changing Dimension Type 2 (SCD Type 2) trên nền tảng Google BigQuery phục vụ hệ thống CellphoneS (170+ cửa hàng).

## 2. Đặc tả Cấu trúc Bảng BigQuery DDL

### 2.1 Bảng Chiều Sản phẩm SCD Type 2 (`int_cellphones.dim_products_scd2`)
- `product_sk` STRING (Khóa thay thế - Primary Key, được tạo bằng `FARM_FINGERPRINT(CONCAT(product_id, '_', valid_from))`)
- `product_id` STRING (Khóa tự nhiên - Natural Key)
- `product_name` STRING (Tên sản phẩm)
- `brand` STRING (Thương hiệu)
- `category` STRING (Danh mục sản phẩm)
- `base_price` NUMERIC (Giá niêm yết tại thời điểm áp dụng)
- `valid_from` DATE (Ngày bắt đầu hiệu lực bản ghi)
- `valid_to` DATE (Ngày kết thúc hiệu lực bản ghi, mặc định `9999-12-31` cho bản ghi hiện tại)
- `is_current` BOOLEAN (Cờ trạng thái: `TRUE` nếu là phiên bản đang hoạt động, `FALSE` nếu là bản ghi lịch sử)

### 2.2 Bảng Sự kiện Bán hàng (`marts_cellphones.fact_sales`)
- `transaction_id` STRING (Mã giao dịch)
- `transaction_date` DATE (Ngày giao dịch - Trường phân vùng Partition)
- `store_id` STRING (Mã cửa hàng - Trường gom nhóm Cluster)
- `product_id` STRING (Mã sản phẩm - Trường gom nhóm Cluster)
- `product_sk` STRING (Khóa thay thế liên kết với bảng `dim_products_scd2` tại thời điểm mua)
- `quantity` INT64 (Số lượng bán)
- `unit_price` NUMERIC (Đơn giá thực tế bán)
- `total_amount` NUMERIC (Tổng tiền giao dịch)

### 2.3 Cơ chế Tối ưu Phân vùng & Gom nhóm (Partitioning & Clustering)
- **Phân vùng (Partitioning)**: Phân vùng theo trường ngày `PARTITION BY transaction_date` để hạn chế dung lượng dữ liệu bị quét (Bytes Scanned).
- **Gom nhóm (Clustering)**: Gom nhóm theo `CLUSTER BY store_id, product_id` để tăng tốc độ xử lý các câu truy vấn lọc theo cửa hàng và sản phẩm.
