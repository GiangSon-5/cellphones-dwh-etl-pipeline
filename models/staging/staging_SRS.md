# Đặc tả Yêu cầu Phần mềm Tầng Staging (SRS)

## 1. Phạm vi Yêu cầu
Tạo lớp trung gian Staging Views trên BigQuery để làm sạch dữ liệu ban đầu, không áp dụng business logic phức tạp nhưng đảm bảo tính toàn vẹn kiểu dữ liệu (data types) và chuẩn hóa tên trường (naming convention).

## 2. Quy tắc & Tiêu chí Nghiệm thu
- Mọi trường ngày tháng phải ép kiểu về `DATE`.
- Mọi giá trị doanh thu, đơn giá phải về `NUMERIC` để loại bỏ sai số số thực (floating point error).
- Loại bỏ các bản ghi missing primary keys.
