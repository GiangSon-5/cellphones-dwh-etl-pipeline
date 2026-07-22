# Đặc tả Yêu cầu Nghiệp vụ Power BI Semantic Model (SRS)

## 1. Bối cảnh Nghiệp vụ & Mục tiêu
Tài liệu này xác định các yêu cầu nghiệp vụ và hiển thị giao diện báo cáo Power BI cho Chuỗi Bán lẻ CellphoneS (170+ cửa hàng).

## 2. Các Chỉ số Hiệu năng Cốt lõi (KPIs)
- **Doanh thu Thu thuần vs Target (Revenue vs Target)**.
- **Tốc độ bán hàng ngày (Daily Run Rate - DRR)**.
- **Số ngày tồn kho an toàn (Inventory to Sales Ratio / Days of Stock)**.
- **Tỷ lệ phân bổ doanh thu theo Vùng Miền & Loại Cửa Hàng (% Revenue Allocation)**.

## 3. Bố cục Giao diện UI/UX & Quy tắc Định dạng Điều kiện
1. **Thẻ Chỉ số Tổng quan (Header Cards)**: Doanh thu thực tế, Target Doanh thu, % Hoàn thành, Số lượng cửa hàng bị cảnh báo cháy hàng.
2. **Bộ Lọc (Slicers)**: Lọc theo Vùng miền (Miền Nam, Miền Bắc...), Loại cửa hàng (A, B, C, D), Danh mục sản phẩm, Khoảng thời gian.
3. **Bảng Báo cáo Vận hành (Main Matrix Visual)**: Danh sách cửa hàng kèm chỉ số DRR, Tồn kho hiện tại, Số ngày tồn kho, và Cờ Cảnh báo Cháy hàng/Đọng vốn (Bật Conditional Formatting định dạng màu đỏ/xanh).
