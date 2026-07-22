# Đặc tả Yêu cầu Phần mềm Tầng Marts (SRS)

## 1. Mục tiêu Nghiệp vụ
Cung cấp các bảng Fact và Dim tinh gọn đã sẵn sàng kết nối với Power BI DirectQuery / Import mode.

## 2. Yêu cầu & Tiêu chí Nghiệm thu
- Đảm bảo tỷ lệ kết nối 1-nhiều (1-to-many) giữa `dim_store`, `dim_product` tới `fact_sales` và `fact_inventory_daily`.
- Cho phép xem nhanh tỷ lệ hoàn thành KPI Doanh thu của từng cửa hàng/khu vực (Khu vực Miền Nam, Miền Bắc, RSM, AM).
