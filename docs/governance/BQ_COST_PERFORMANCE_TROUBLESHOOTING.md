# Hướng dẫn Xử lý Sự cố Chi phí & Hiệu năng Truy vấn Google BigQuery
## Phần 4 Đề bài Đánh giá: Quản trị Hệ thống & Kịch bản Xử lý Sự cố (Quy mô 170+ Cửa hàng)

---

## 1. Tổng quan Bài toán Chi phí & Hiệu năng BigQuery (Quy mô CellphoneS)

Với quy mô 170+ cửa hàng CellphoneS phát sinh hàng triệu giao dịch mỗi ngày, nếu không quản trị BigQuery đúng cách, doanh nghiệp sẽ gặp 2 bài toán lớn:
1. **Bùng nổ Chi phí Query (Cost Spike)**: BigQuery tính phí dựa trên **Dung lượng dữ liệu bị quét (Bytes Scanned)** ở mô hình On-Demand ($6.25/TB quét).
2. **Nghẽn Hiệu năng (Query Timeout / High Slot Consumption)**: Các truy vấn dashboard Power BI bị chậm do Full Table Scan hoặc nghẽn bộ nhớ Shuffle khi thực hiện Join bảng lớn.

---

## 2. Chiến lược Tối ưu Chi phí (Cost Optimization Strategy)

### 2.1 Bắt buộc Phân vùng & Gom nhóm (Partitioning & Clustering)
- **Quy tắc bắt buộc**: 100% các bảng Fact (`fact_sales`, `fact_inventory_daily`) phải được **Phân vùng theo Ngày (`transaction_date`, `log_date`)** và **Gom nhóm theo `store_id`, `product_id`**.
- **Hiệu quả**: 
  - Khi Power BI query doanh thu ngày hôm qua của Cửa hàng ST001, BigQuery chỉ quét duy nhất 1 partition ngày hôm qua thay vì quét toàn bộ lịch sử 3 năm (Giảm **95% - 99%** dung lượng dữ liệu bị quét).
- **Ràng buộc Filter Phân vùng**: Thiết lập cài đặt `Require partition filter = TRUE` trong BigQuery DDL để ngăn ngừa các câu truy vấn `SELECT * FROM fact_sales` không có điều kiện `WHERE`.

```sql
-- Cài đặt ngăn chặn truy vấn không có filter partition
ALTER TABLE `cellphones-analytics-prod.marts_cellphones.fact_sales`
SET OPTIONS (require_partition_filter = true);
```

### 2.2 Loại bỏ Anti-Pattern `SELECT *` & Sử dụng Materialized Views
- **Tránh Anti-Pattern**: Viết `SELECT *` trong Power BI SQL Native Query khiến BigQuery phải đọc tất cả các cột. Chỉ chọn đúng các cột cần thiết.
- **Materialized Views**: Xây dựng Materialized View tự động refresh cho các phép gom nhóm doanh thu cửa hàng theo tháng (`marts_sales_performance`). BigQuery sẽ tự động cache kết quả tính toán sẵn.

### 2.3 Cấu hình BigQuery BI Engine & Slot Commitments
- Bật **BigQuery BI Engine** với dung lượng RAM dành riêng (từ 10 GB đến 50 GB) cho dataset `marts_cellphones`.
- BI Engine tự động lưu bộ nhớ RAM sub-second cho các truy vấn lặp lại từ Power BI dashboards, giúp thời gian phản hồi dashboard dưới 500ms và không tốn chi phí scan lại dữ liệu.

---

## 3. Kịch bản Xử lý Sự cố & Tối ưu Hiệu năng (Incident Playbook)

### Kịch bản 1: Query Dashboard Power BI Bị Chậm (> 30 giây)
- **Nguyên nhân**: Power BI tạo query không tận dụng được Partition Pruning do ép kiểu `CAST(transaction_date AS STRING)` trong mệnh đề `WHERE`.
- **Khắc phục**: 
  1. Mở BigQuery Execution Details -> Kiểm tra chỉ số `Bytes Scanned` và `Slot Time Consumed`.
  2. Sửa lại câu SQL trong Power BI Semantic Model để giữ nguyên kiểu `DATE` trong điều kiện `WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)`.

### Kịch bản 2: Chi phí Quét Dữ liệu Tăng Đột Biến (Spike Alert)
- **Nguyên nhân**: Đội Analysts chạy ad-hoc query join bảng `fact_sales` với `fact_inventory_daily` không có chìa khóa gom nhóm `store_id`, dẫn đến phép nhân bản ghi (Cartesian Product / Cross Join).
- **Khắc phục**: 
  1. Cấu hình BigQuery Custom Quota: Giới hạn tối đa **10 GB/query** đối với tài khoản Analysts.
  2. Hướng dẫn nhóm Analyst sử dụng bảng trung gian aggregated `int_daily_inventory_sales` đã được tổng hợp sẵn.
