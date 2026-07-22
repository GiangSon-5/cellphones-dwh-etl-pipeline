# Đặc tả Yêu cầu Phần mềm Module Power BI (SRS)

## 1. Mục tiêu Nghiệp vụ
Xây dựng Dashboard Vận hành Chuỗi Bán lẻ Điện thoại CellphoneS giúp Ban Giám đốc và RSM/AM:
- Theo dõi doanh thu thực tế so với Target theo từng Khu vực (Miền Nam, Miền Bắc...).
- Nhận cảnh báo tức thời các mặt hàng có nguy cơ cháy hàng ($\le 2$ ngày tồn kho) hoặc tồn kho đọng vốn ($\ge 30$ ngày).

## 2. Yêu cầu Phân bổ Doanh thu Động (Dynamic Revenue Allocation)
Bảng ảo DAX `vtable_RegionalRevenueAllocation` tự động phân bổ tỷ trọng doanh thu (% Revenue Allocation) của từng vùng miền trên tổng doanh thu toàn chuỗi khi người dùng tương tác với Slicer trên báo cáo.
