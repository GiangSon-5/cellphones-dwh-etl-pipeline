# Đặc tả Kỹ thuật Quản trị & Tối ưu Chi phí BigQuery (SPEC)

## 1. Quy định Quản trị Hệ thống
- **Hạn ngạch Quét Dữ liệu tối đa (Max Scanned Bytes per Query Quota)**: 10 GB cho môi trường Ad-hoc Analytics.
- **Ràng buộc Phân vùng (Partition Constraint)**: Bắt buộc cài đặt `require_partition_filter = true` trên tất cả các bảng Fact thuộc tầng Marts.
- **Chính sách Cache (Cache Policy)**: Bật `use_query_cache = true` cho toàn bộ kết nối BI.
- **Dung lượng BI Engine**: Đăng ký tối thiểu 10 GB In-Memory BI Engine cho dataset `marts_cellphones`.
