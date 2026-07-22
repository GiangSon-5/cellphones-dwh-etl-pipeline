# Đặc tả Kỹ thuật Module Power BI (SPEC)

## 1. Tổng quan
Thư mục `powerbi/` chứa mã nguồn **DAX Measures**, **DAX Virtual Tables** và **Semantic Model JSON** định nghĩa toàn bộ mô hình dữ liệu cho Dashboard Vận hành chuỗi 170+ cửa hàng CellphoneS.

## 2. Kiến trúc & Nguyên tắc Thiết kế
- **Chuẩn Star Schema**: Đảm bảo mối quan hệ 1 - Nhiều (1-to-many) chiều lọc một hướng (Single Direction Filtering) từ Dim sang Fact để tối ưu hóa Tabular Engine.
- **Bảng Dữ liệu Chiều (Dimensions)**: `dim_store`, `dim_product`.
- **Bảng Dữ liệu Sự kiện (Facts)**: `fact_sales`, `fact_inventory_daily`.
- **Tối ưu DAX**: Tránh dùng hàm `CALCULATE` vô điều kiện bên trong các vòng lặp; ưu tiên sử dụng `DIVIDE` thay cho phép chia `/` để tránh lỗi Division by Zero.
