# Đặc tả Kỹ thuật Tầng Staging (SPEC)

## 1. Tổng quan
Lớp Staging (`stg_cellphones`) phản ánh 1:1 với dữ liệu thô từ hệ thống nguồn (POS/ERP/Inventory Log). Lớp này thực hiện chuẩn hóa kiểu dữ liệu (data typing), đổi tên cột theo chuẩn snake_case và loại bỏ các bản ghi trùng lặp/null khóa chính.

## 2. Đặc tả Views & Schemas
- `stg_transactions`: Chứa giao dịch bán hàng chi tiết (`transaction_id`, `transaction_date`, `product_id`, `store_id`, `quantity`, `unit_price`, `total_amount`).
- `stg_inventory`: Chứa nhật ký tồn kho daily (`log_date`, `store_id`, `product_id`, `beginning_inventory`, `received_quantity`, `sold_quantity`, `ending_inventory`).
- `stg_stores`: Chứa master dữ liệu cửa hàng (`store_id`, `store_name`, `region`, `regional_sales_manager`, `area_manager`, `store_type`).
- `stg_products`: Master sản phẩm (`product_id`, `product_name`, `brand`, `category`, `base_price`).
- `stg_targets`: Chỉ tiêu doanh thu theo tháng (`store_id`, `month_year`, `target_revenue`).
