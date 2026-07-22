# Đặc tả Kỹ thuật Module ETL Pipeline (SPEC)

## 1. Tổng quan Module
Module `src/pipeline` chịu trách nhiệm thu thập, làm sạch, biến đổi dữ liệu thô (.csv) và tính toán các chỉ số kinh doanh quan trọng: `Daily_Run_Rate` (DRR) và `Inventory_to_Sales_Ratio` cho chuỗi 170+ cửa hàng CellphoneS.

## 2. Đặc tả Thành phần & API

### 2.1 `DataCleaner` (`src/pipeline/cleaner.py`)
- **Đầu vào (Inputs)**: Đường dẫn đến thư mục chứa 5 file dữ liệu thô: `Transactions.csv`, `Inventory_Logs.csv`, `Store_Info.csv`, `Products.csv`, `Targets.csv`.
- **Logic xử lý**:
  - Ép kiểu dữ liệu `Date`, `Log_Date` sang `datetime64[ns]`.
  - Khử trùng lặp theo Khóa chính (`Transaction_ID`, `(Log_Date, Store_ID, Product_ID)`).
  - Tự động điền/tính toán `Ending_Inventory` thiếu hụt: `Beginning + Received - Sold`.
  - Kiểm tra miền giá trị số âm (clip giá trị âm về 0).

### 2.2 `MetricsCalculator` (`src/pipeline/metrics_calculator.py`)
- **`calculate_daily_run_rate(sales_df, group_cols)`**:
  - Công thức: $\text{Daily Run Rate (DRR)} = \frac{\sum \text{Quantity}}{\text{Max(Date)} - \text{Min(Date)} + 1}$
  - Trả về DataFrame chứa `Daily_Run_Rate` (số lượng/ngày) và `Daily_Revenue_Run_Rate` (doanh thu/ngày).
- **`calculate_inventory_to_sales_ratio(inventory_df, drr_df)`**:
  - Công thức: $\text{Inventory to Sales Ratio} = \frac{\text{Ending Inventory}}{\text{Daily Run Rate}}$
  - Trả về số ngày bán của lượng tồn kho hiện tại (Days of Inventory / Stock Cover). Tránh lỗi chia cho 0 bằng cách gán indicator 999.0 cho sản phẩm không phát sinh doanh số.

### 2.3 `DataTransformer` (`src/pipeline/transformer.py`)
- **Điều phối (Orchestration)**: Tích hợp DataCleaner + MetricsCalculator + ConfigDrivenShopClassifier.
- **Đầu ra (Data Outputs)**: Xuất 6 tập dữ liệu sạch tại `data/processed/`.

## 3. Cấu trúc Tập Dữ liệu Đầu ra (`data/processed/`)
- `processed_transactions.csv`: Giao dịch bán hàng chi tiết đã làm sạch và bổ sung master data.
- `processed_inventory.csv`: Nhật ký tồn kho kèm `Daily_Run_Rate` & `Inventory_to_Sales_Ratio`.
- `processed_stores.csv`: Thông tin cửa hàng kèm `Dynamic_Classification` và `Avg_Monthly_Revenue`.
- `store_performance.csv`: Doanh thu hàng tháng, target và `Achievement_Pct`.
- `daily_run_rate.csv`: DRR chi tiết theo từng Cửa hàng và Sản phẩm.
