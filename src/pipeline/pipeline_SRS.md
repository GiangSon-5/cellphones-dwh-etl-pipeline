# Đặc tả Yêu cầu Phần mềm Module Pipeline (SRS)

## 1. Mục tiêu Nghiệp vụ & Phạm vi
Cung cấp luồng dữ liệu tự động (ETL Data Pipeline) cho Phòng Analytics và Ban Điều hành Chuỗi Bán lẻ CellphoneS. Pipeline chuẩn hóa dữ liệu từ hệ thống POS/ERP cửa hàng, phục vụ báo cáo vận hành hàng ngày và cảnh báo kho.

## 2. Yêu cầu Nghiệp vụ & Case Sử dụng

### UC-01: Chuẩn hóa Dữ liệu Giao dịch & Tồn kho
- **Tác nhân**: Hệ thống / Data Pipeline.
- **Kích hoạt**: Chạy định kỳ daily hoặc thực thi qua runner CLI.
- **Quy tắc Nghiệp vụ**:
  - Dữ liệu trùng giao dịch do nghẽn mạng POS phải bị loại bỏ dựa trên `Transaction_ID`.
  - Tồn kho cuối ngày (`Ending_Inventory`) nếu thiếu trong file log phải được tự động hồi phục dựa trên công thức xuất nhập tồn: $\text{Tồn đầu} + \text{Nhập} - \text{Bán}$.

### UC-02: Tính toán Chỉ số Daily Run Rate (Tốc độ bán hàng ngày)
- **Nhu cầu Nghiệp vụ**: Đo lường trung bình 1 cửa hàng bán được bao nhiêu sản phẩm X trong một ngày để dự báo nhu cầu đặt hàng.
- **Tiêu chí Nghiệm thu**: Tốc độ bán được tính theo ngày hoạt động thực tế, không bị lệch khi cửa hàng mới khai trương giữa tháng.

### UC-03: Cảnh báo Tồn kho & Tỷ lệ Tồn kho / Bán hàng (Inventory-to-Sales Ratio)
- **Nhu cầu Nghiệp vụ**: Nhận biết ngay cửa hàng nào sắp cháy hàng (Stockout) hoặc bị đọng vốn tồn kho quá nhiều (Overstock).
- **Tiêu chí Nghiệm thu**: Tỷ lệ tồn kho/bán hàng $\le 2.0$ ngày lập tức gắn cờ Cảnh báo Cháy hàng.
