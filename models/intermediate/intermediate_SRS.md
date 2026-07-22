# Đặc tả Yêu cầu Phần mềm Tầng Intermediate (SRS)

## 1. Bài toán Nghiệp vụ & Mục tiêu
1. **Lưu trữ Lịch sử Giá Sản phẩm (SCD Type 2)**: Điện thoại và phụ kiện thường xuyên thay đổi giá niêm yết (Base Price) theo các chương trình khuyến mãi/ra mắt sản phẩm mới. Cần lưu lại chính xác lịch sử giá tại thời điểm phát sinh giao dịch thay vì ghi đè.
2. **Theo dõi Tốc độ Bán trượt 30 ngày (Moving DRR)**: Đảm bảo chỉ số Daily Run Rate không bị nhiễu do biến động đột biến của một ngày lẻ.

## 2. Tiêu chí Nghiệm thu
- Mọi sự thay đổi về giá `base_price` của `Product_ID` phải tạo ra 1 dòng bản ghi mới với `is_current = TRUE` và chuyển bản ghi cũ về `is_current = FALSE`.
- Các giao dịch lịch sử khi join với `dim_products_scd2` theo điều kiện `transaction_date BETWEEN valid_from AND valid_to` phải khớp đúng đơn giá lịch sử.
