# Đặc tả Yêu cầu Phần mềm Module Classifiers (SRS)

## 1. Bài toán Nghiệp vụ (Yêu cầu Phần 4 Đề bài)
Hệ thống cũ phân loại cửa hàng bị hardcode trực tiếp vào code Python/SQL, dẫn đến mỗi khi Phòng Business (Sales Ops) thay đổi tiêu chí phân hạng cửa hàng hoặc ngưỡng KPIs, đội Data Engineering phải sửa code, chạy lại CI/CD pipeline và có nguy cơ gây lặp lại lỗi hoặc sai lệch dữ liệu lịch sử.

## 2. Yêu cầu & Khả năng Chức năng

### FR-01: Tách biệt Quy tắc Nghiệp vụ bằng Cấu hình (Config-driven)
- **Yêu cầu**: Tách biệt 100% quy tắc nghiệp vụ khỏi mã thực thi Python.
- **Tiêu chí Nghiệm thu**: Toàn bộ tiêu chí phân loại cửa hàng, ngưỡng KPIs, và thang cảnh báo tồn kho nằm tại `configs/shop_classifier.yaml`.

### FR-02: Phân hạng Cửa hàng Động (Dynamic Shop Classification)
- Phân loại 170+ cửa hàng thành 4 nhóm chính:
  1. **Flagship Store**: Doanh thu trung bình tháng $\ge 1.2$ Tỷ VND hoặc Store_Type A.
  2. **Key Store**: Doanh thu trung bình tháng $\ge 800$ Triệu VND hoặc Store_Type B.
  3. **Standard Store**: Doanh thu trung bình tháng $\ge 400$ Triệu VND hoặc Store_Type C.
  4. **Micro Store**: Cửa hàng quy mô nhỏ / mới mở.

### FR-03: Cảnh báo Tồn kho & Đánh giá Hoàn thành Target
- Tự động gắn nhãn mức độ hoàn thành Target (% Target Revenue) và chỉ số an toàn tồn kho theo quy tắc động.
