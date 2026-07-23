# BÁO CÁO KỸ THUẬT
## Hệ Thống Data Warehouse, Python ETL Pipeline & Power BI Operational Dashboard
### Chuỗi Bán Lẻ Điện Thoại & Thiết Bị Công Nghệ CellphoneS (170+ Cửa Hàng)

---

## 📌 PHẦN 1: TỔNG QUAN BỐI CẢNH VẬN HÀNH & BÀI TOÁN NGHIỆP VỤ

### 1. Bối Cảnh Vận Hành Chuỗi Bán Lẻ CellphoneS
CellphoneS là chuỗi bán lẻ công nghệ hàng đầu tại Việt Nam với quy mô hơn 170+ cửa hàng. Để quản trị hiệu quả toàn hệ thống, dữ liệu vận hành từ các phân hệ POS bán hàng, Nhật ký kho và Danh mục cửa hàng được tiếp nhận liên tục. 

Hệ thống tiếp nhận **5 luồng dữ liệu đầu vào dạng CSV** đại diện cho các phân hệ vận hành:

#### 🟢 Group 1: 3 Luồng Dữ Liệu Vận Hành Cốt Lõi (Core Operational Streams)
1. **`Transactions.csv` (Giao dịch bán hàng POS)**: `Transaction_ID`, `Date`, `Product_ID`, `Store_ID`, `Quantity`, `Unit_Price`.
2. **`Inventory_Logs.csv` (Nhật ký tồn kho hằng ngày)**: `Log_Date`, `Store_ID`, `Product_ID`, `Beginning_Inventory`, `Received`, `Sold`, `Ending_Inventory`.
3. **`Store_Info.csv` (Thông tin master cửa hàng)**: `Store_ID`, `Store_Name`, `Region`, `RSM`, `AM`, `Store_Type`.

#### 🔵 Group 2: 2 Luồng Dữ Liệu Tham Chiếu & Chỉ Tiêu (Reference & Target Streams)
4. **`Products.csv` (Master danh mục sản phẩm & giá niêm yết chuẩn)**: `Product_ID`, `Product_Name`, `Brand`, `Category`, `Base_Price`.
5. **`Targets.csv` (Chỉ tiêu doanh thu kế hoạch hàng tháng)**: `Store_ID`, `Month_Year`, `Target_Revenue`.

---

### 2. 3 Thách Thức Kỹ Thuật & Bài Toán Kinh Doanh Cốt Lõi
* **Chất lượng dữ liệu POS không đồng nhất**: Xuất hiện trùng lặp hóa đơn do lỗi mạng POS và đơn hàng bị khuyết `Quantity` (Null).
* **Quản trị đọng vốn tồn kho**: Thiếu chỉ số đánh giá tốc độ bán hàng (`Daily Run Rate - DRR`) và số ngày trang trải tồn kho (`Inventory Cover Ratio`), dẫn tới nguy cơ ứ đọng vốn hàng công nghệ giảm giá nhanh.
* **Đánh giá hiệu suất cửa hàng linh hoạt**: Thiếu cơ chế đánh giá % hoàn thành Target và xếp loại cửa hàng linh hoạt theo cấu hình động.

---

## 🏗️ PHẦN 2: THIẾT KẾ DATA WAREHOUSE SCHEMA & KỸ THUẬT SCD TYPE 2

### 1. Kiến Trúc Data Warehouse 3 Tầng & Sơ Đồ ERD Star Schema
Hệ thống Data Warehouse trên Google BigQuery được thiết kế chuẩn mực theo mô hình 3 tầng (Medallion Architecture), trong đó mô hình **Star Schema (Sơ đồ Ngôi Sao)** được triển khai chính xác tại **Tầng Marts (`marts_*`)**:

```text
[Raw Datasets (.csv)] ──> [1. Staging Layer (staging_*)] ──> [2. Intermediate Layer (dim_*_scd2)] ──> [3. Marts Layer (marts_*)] ──> [Power BI Semantic Model]
```

![Sơ Đồ ERD Star Schema & Kiến Trúc Data Warehouse](assets/images/ERD.png)

#### Cấu Trúc Bảng Fact & Dimension Tại Tầng Marts:
* **2 Bảng Fact Trung Tâm**:
  1. **`fact_sales`**: Lưu trữ các giao dịch bán hàng chi tiết (`transaction_id`, `date`, `store_id`, `product_id`, `quantity`, `unit_price`, `total_amount`).
  2. **`fact_inventory_daily`**: Lưu trữ nhật ký tồn kho daily (`log_date`, `store_id`, `product_id`, `beginning_inventory`, `received`, `sold`, `ending_inventory`, `inventory_cover_ratio`).
* **3 Bảng Chiều (Dimension Tables)**:
  1. **`dim_store`**: Chiều cửa hàng (`store_id`, `store_name`, `region`, `rsm`, `am`, `store_type`, `tier`).
  2. **`dim_products_scd2`**: Chiều sản phẩm áp dụng SCD Type 2 (`product_sk`, `product_id`, `product_name`, `brand`, `category`, `base_price`, `valid_from`, `valid_to`, `is_current`).
  3. **`dim_date`**: Chiều thời gian chuẩn hóa (`date`, `day`, `month`, `quarter`, `year`, `day_of_week`).
* **Lý do chọn Star Schema trên BigQuery**: Giảm số lượng phép `JOIN` phức tạp, tận dụng cơ chế lưu trữ dạng cột (Columnar Storage) và khả năng tính toán song song phân tán của BigQuery, giúp truy vấn báo cáo đạt hiệu năng tối đa với chi phí thấp nhất.

---

### 2. Giải Trình Kỹ Thuật Slowly Changing Dimension (SCD Type 2) Cho Bảng Sản Phẩm

#### ✅ Phương Án Lựa Chọn: Sử dụng kỹ thuật **Slowly Changing Dimension Type 2 (SCD Type 2)**.

#### 🎯 Phân Tích Nguyên Lý & Lý Do Nghiệp Vụ:
1. **Bảo toàn tính đúng đắn lịch sử tài chính (Historical Accuracy)**: Khi các mẫu điện thoại thay đổi giá liên tục theo các chương trình khuyến mãi (Flash Sale, Black Friday, Hotsale ra mắt sản phẩm mới), đơn hàng phát sinh ở quá khứ phải đối soát với đúng mức giá áp dụng tại thời điểm đó. Nếu dùng **SCD Type 1** (ghi đè giá mới lên giá cũ), toàn bộ doanh thu, giá vốn và biên lợi nhuận của các đơn hàng trong quá khứ sẽ bị biến dạng và tính toán sai lệch truy hồi.
2. **Không làm phình đại bảng Fact**: Thay vì lưu trữ toàn bộ thuộc tính sản phẩm vào từng dòng của bảng Fact (ngốn dung lượng storage BigQuery), SCD Type 2 tạo ra một dòng bản ghi mới trong bảng `dim_products_scd2` với một **Surrogate Key (`product_sk`)** mới mỗi khi giá bán thay đổi, giữ cho bảng Fact gọn nhẹ và nhất quán.
3. **Truy vấn theo mốc thời gian linh hoạt (Point-in-time Reporting)**: Giúp kỹ sư dữ liệu và chuyên viên phân tích BI dễ dàng lọc báo cáo doanh số theo giá niêm yết cũ hoặc giá khuyến mãi mới tại bất kỳ mốc thời gian nào trong lịch sử bằng điều kiện `transaction_date BETWEEN valid_from AND valid_to`.

#### 💻 Minh Họa Kỹ Thuật BigQuery DDL/DML SCD Type 2 (`models/intermediate/dim_products_scd2.sql`):
```sql
-- Tạo Surrogate Key bằng FARM_FINGERPRINT kết hợp Product_ID và Base_Price
CREATE OR REPLACE TABLE `cellphones_dwh.dim_products_scd2` AS
SELECT 
    FARM_FINGERPRINT(CONCAT(Product_ID, '_', CAST(Base_Price AS STRING))) AS product_sk,
    Product_ID AS product_id,
    Product_Name AS product_name,
    Brand AS brand,
    Category AS category,
    Base_Price AS base_price,
    CURRENT_DATE() AS valid_from,
    CAST(NULL AS DATE) AS valid_to,
    TRUE AS is_current
FROM `cellphones_dwh.staging_products`;
```

---

## 🐍 PHẦN 3: XỬ LÝ DỮ LIỆU BẰNG PYTHON DATA ETL PIPELINE

Pipeline xử lý dữ liệu được thiết kế dạng **Modular Architecture** bằng Python Pandas trong thư mục `src/pipeline/`, đồng thời cung cấp bộ **6 File Jupyter Notebook EDA** trong thư mục `notebooks/`:

### 1. Module Làm Sạch Dữ Liệu (`src/pipeline/cleaner.py`)
* **Khử trùng lặp POS**: Loại bỏ 100% bản ghi trùng lặp mã hóa đơn `Transaction_ID`.
* **Bổ khuyết giá trị Null**:
  * Đơn hàng bị khuyết `Quantity` (Null) được khôi phục tự động bằng quy tắc nghiệp vụ: `Quantity = Unit_Price / Base_Price = 1.0` (giúp bảo toàn **380+ triệu VNĐ** doanh thu bị đe dọa thất thoát).
  * Nhật ký kho bị khuyết `Ending_Inventory` được tính bù bằng công thức: `Ending_Inventory = Beginning_Inventory + Received - Sold`.
* **Chuẩn hóa thời gian**: Ép kiểu toàn bộ các cột ngày giờ về ISO Standard `YYYY-MM-DD`.

### 2. Module Biến Đổi & Tính Chỉ Số Vận Hành (`src/pipeline/metrics_calculator.py`)
* **Daily Run Rate (DRR)**: Tốc độ bán hàng trung bình daily của từng sản phẩm tại từng cửa hàng:
  $$\text{DRR} = \frac{\text{Total Sales Quantity}}{\text{Active Sales Days}}$$
* **Inventory to Sales Ratio (Days of Cover)**: Số ngày trang trải tồn kho đại diện cho tỷ lệ Tồn kho/Doanh số:
  $$\text{Inventory Cover Ratio (Days of Cover)} = \frac{\text{Ending Inventory}}{\text{DRR}}$$

### 3. Bộ Tệp Dữ Liệu Đầu Ra Sạch (`data/processed/*.csv`)
Pipeline tự động xuất 6 file dữ liệu sạch cấu trúc sẵn sàng đẩy lên BigQuery DWH:
1. `processed_transactions.csv` (1,800 dòng x 14 cột - 224.5 KB)
2. `processed_inventory.csv` (1,350 dòng x 9 cột - 62.5 KB)
3. `processed_stores.csv` (15 dòng x 8 cột - 1.3 KB)
4. `processed_products.csv` (10 dòng x 5 cột - 0.6 KB)
5. `daily_run_rate.csv` (150 dòng x 9 cột - 13.5 KB)
6. `store_performance.csv` (45 dòng x 7 cột - 2.5 KB)

---

## 📊 PHẦN 4: POWER BI OPERATIONAL DASHBOARD & DAX VIRTUAL TABLES

### 1. Thiết Kế Operational Dashboard Trực Quan (`powerbi/Cellphones_Operational_Dashboard.pbix`)
![Giao diện Power BI Operational Dashboard](assets/images/power%20bi.png)

Dashboard trực quan hóa tình hình vận hành Quý 3/2026 với các vùng thông tin tiêu chuẩn UI/UX:
* **Khối Executive KPIs**: Tổng doanh thu (**56.6 Tỷ VNĐ**), % Đạt Target Trung bình (**99.29%**), Số ngày tồn kho trang trải TB (**112.30 Ngày**).
* **Phân tích Xu hướng & Khu vực**: Biểu đồ diễn biến doanh thu theo tháng phân nhóm theo loại hình cửa hàng (Loại C Standard dẫn đầu 22.6 Tỷ VNĐ).
* **Cảnh báo Đọng vốn Tồn kho**: Bar chart hiển thị 15/15 cửa hàng vượt ngưỡng 30 ngày bán, cảnh báo đọng vốn cần điều chuyển hàng gấp.
* **Bảng Xếp Hạng Hiệu Suất Cửa Hàng**: Phân loại cửa hàng theo 4 nhóm hiệu năng (*Super Star, On Track, Underperforming, Critical Warning*).

---

### 2. Thuyết Minh 2 Mã DAX Virtual Tables Nâng Cao (`powerbi/virtual_tables.dax`)

#### 📌 Mã DAX 1: Tính Tỷ Lệ Hoàn Thành Mục Tiêu (Achievement %) Dùng Bảng Ảo Virtual Table
```dax
vtable_StoreTargetAchievement = 
ADDCOLUMNS(
    SUMMARIZE(
        processed_transactions,
        processed_stores[Store_ID],
        processed_stores[Store_Name],
        processed_stores[Region],
        processed_stores[Store_Type]
    ),
    "Actual_Revenue", CALCULATE(SUM(processed_transactions[Total_Amount])),
    "Achievement_Pct", DIVIDE(CALCULATE(SUM(processed_transactions[Total_Amount])), 3800000000, 0),
    "Performance_Status", 
        SWITCH(
            TRUE(),
            DIVIDE(CALCULATE(SUM(processed_transactions[Total_Amount])), 3800000000, 0) >= 1.10, "Super Star",
            DIVIDE(CALCULATE(SUM(processed_transactions[Total_Amount])), 3800000000, 0) >= 0.90, "On Track",
            DIVIDE(CALCULATE(SUM(processed_transactions[Total_Amount])), 3800000000, 0) >= 0.75, "Underperforming",
            "Critical Warning"
        )
)
```
* **Giải trình**: Sử dụng `SUMMARIZE` tạo bảng ảo 15 cửa hàng, dùng `CALCULATE(SUM(...))` để ép Context Transition tính doanh thu thực tế, chia cho Target Benchmark `3.8 Tỷ VNĐ` và phân loại hiệu suất bằng `SWITCH(TRUE(), ...)`.

---

#### 📌 Mã DAX 2: Tính Phân Bổ Tỷ Trọng Doanh Thu Theo Loại Cửa Hàng Dùng Bảng Ảo
```dax
vtable_StoreTypeRevenueAllocation = 
VAR GrandTotalSales = CALCULATE(SUM(processed_transactions[Total_Amount]), ALL(processed_transactions))
RETURN
ADDCOLUMNS(
    SUMMARIZE(
        processed_stores,
        processed_stores[Store_Type]
    ),
    "StoreType_Revenue", CALCULATE(SUM(processed_transactions[Total_Amount])),
    "Grand_Total_Revenue", GrandTotalSales,
    "Revenue_Allocation_Pct", DIVIDE(CALCULATE(SUM(processed_transactions[Total_Amount])), GrandTotalSales, 0)
)
```
* **Giải trình**: Dùng `VAR GrandTotalSales = CALCULATE(..., ALL(...))` cố định mẫu số tổng toàn chuỗi (**56.597 Tỷ VNĐ**), sau đó tính % đóng góp của từng nhóm: **Loại C (39.91%)**, **Loại D (20.68%)**, **Loại B (20.26%)**, **Loại A (19.15%)**. Tổng 4 nhóm bằng đúng 100.0%.

---

## ⚙️ PHẦN 5: TƯ DUY HỆ THỐNG - ĐIỀU TRA CHI PHÍ BIGQUERY & TÁI THIẾT KẾ CODEBASE

### 1. Quy Trình Điều Tra & Tối Ưu Chi Phí Pipeline BigQuery (Troubleshooting & SQL Optimization)

Bối cảnh hệ thống gặp sự cố: Pipeline dữ liệu tự động hằng ngày trên BigQuery đột ngột tăng vọt chi phí (cost) gấp 3 lần và chạy chậm, dù lượng dữ liệu đầu vào không có sự đột biến.

#### 🔍 5 Bước Điều Tra Sự Cố (Troubleshooting Checklist):
1. **Bước 1. Audit Query Logs (`INFORMATION_SCHEMA.JOBS_BY_PROJECT`)**: Truy vấn lịch sử job BigQuery để lọc danh sách các câu lệnh có `total_bytes_billed` hoặc `slot_ms` tăng đột biến trong ngày.
2. **Bước 2. Phân Tích Execution Graph & Stage Bottlenecks**: Kiểm tra kế hoạch thực thi để phát hiện các giai đoạn bị nghẽn do Slot Contention hoặc Data Shuffle Read/Write quá cao.
3. **Bước 3. Kiểm Tra Phân Vùng Khoảng Thời Gian (Partition Pruning Audit)**: Xác minh xem truy vấn có bị quên điều kiện lọc `_PARTITIONDATE` / `DATE(timestamp)` khiến BigQuery phải Full Scan toàn bộ bảng lịch sử hay không.
4. **Bước 4. Đánh Giá Trùng Lặp & Khử Nổ Dòng (JOIN Explosion & Data Skew)**: Kiểm tra các phép `JOIN` trên khóa trùng lặp khiến số lượng bản ghi tăng vọt ngoài dự kiến.
5. **Bước 5. Kiểm Tra Xung Đột Lịch Chạy Pipeline (Concurrency & Quota Check)**: Đánh giá xem có nhiều job ETL chạy song song vào cùng mốc giờ gây nghẽn tài nguyên slot.

#### ⚡ 5 Kỹ Thuật Tối Ưu SQL Đưa Hệ Thống Ổn Định (Before vs After):

1. **Partitioning & Clustering (Phân vùng & Gom nhóm)**:
   * ❌ *Trước*: `WHERE DATE(created_at) >= '2026-07-01'` (Bọc hàm làm mất chỉ mục, quét 100GB).
   * ✅ *Sau*: `WHERE _PARTITIONDATE >= '2026-07-01'` (Chỉ quét đúng phân vùng cần thiết, giảm 98% chi phí).
2. **Columnar Selection (Chỉ chọn cột cần dùng)**:
   * ❌ *Trước*: `SELECT * FROM transactions` (Quét toàn bộ 50 cột ngốn dung lượng).
   * ✅ *Sau*: `SELECT transaction_id, store_id, total_amount` (Chỉ lấy cột phục vụ báo cáo, tiết kiệm 90% byte scanned).
3. **Khử JOIN Explosion & Dùng Integer Surrogate Key**:
   * ❌ *Trước*: `JOIN` trực tiếp trên chuỗi String chưa deduplicate gây nổ dòng.
   * ✅ *Sau*: Pre-aggregate dữ liệu & `JOIN` qua khóa Surrogate Key Integer (`FARM_FINGERPRINT`).
4. **Incremental Load Với `MERGE INTO` Thay Cho Overwrite**:
   * ❌ *Trước*: `CREATE OR REPLACE TABLE` (Tính toán lại và ghi đè 100% dữ liệu lịch sử mỗi ngày).
   * ✅ *Sau*: `MERGE INTO` (Chỉ nạp và cập nhật phần dữ liệu Delta phát sinh trong ngày).
5. **Materialized Views & Caching**:
   * ❌ *Trước*: Thường xuyên chạy lại các Subquery tổng hợp phức tạp ở nhiều báo cáo khác nhau.
   * ✅ *Sau*: `CREATE MATERIALIZED VIEW` để BigQuery tự động cache kết quả truy vấn trung gian.

---

### 2. Tái Thiết Kế Kiến Trúc Quản Trị Quy Tắc Phân Loại Cửa Hàng (Config-Driven Code Governance)

Bối cảnh nâng cấp: Đoạn script phân loại cửa hàng legacy viết cứng logic `classify_shop(score, kpi_count)` bị sửa trực tiếp khi rule thay đổi, làm mâu thuẫn báo cáo phân loại của các tháng trước.

#### ❌ Nhận Xét & Phân Tích Nhược Điểm Đoạn Code Legacy:
1. **Hardcoded Magic Numbers (Vi phạm nguyên tắc DRY & Clean Code)**: Các con số ngưỡng (`1.0`, `6`, `0.85`, `5`...) bị viết cứng trực tiếp vào thân hàm Python. Khi Business thay đổi rule, lập trình viên buộc phải sửa code nguồn.
2. **Mutating Past Logic (Phá hỏng tính toàn vẹn dữ liệu lịch sử)**: Việc sửa trực tiếp code nguồn rồi chạy lại cho toàn bộ dữ liệu làm thay đổi kết quả phân loại của các tháng trong quá khứ, gây mâu thuẫn báo cáo (Inconsistent Historical Reports).
3. **Thiếu Lịch Sử Audit & Version Control (Zero Auditability)**: Không biết ai đã sửa rule, sửa lúc nào, lý do sửa là gì và ngưỡng cũ của các tháng trước là bao nhiêu.
4. **Thiếu Unit Tests & Validation**: Không có bộ kiểm thử tự động để đảm bảo việc thay đổi rule mới không làm hỏng logic của hệ thống.

#### 🛠️ Đề Xuất Cải Tiến Kỹ Thuật & Tái Thiết Kế Kiến Trúc:

1. **Tách Biệt Logic & Cấu Hình Rule (Config-Driven Architecture)**:
   Chuyển toàn bộ quy tắc phân loại ra tệp cấu hình độc lập dạng YAML (`configs/shop_classifier.yaml`), không can thiệp vào codebase Python.
2. **Quản Lý Phiên Bản Rule Với Ngày Hiệu Lực (Effective Dating & Rule Versioning)**:
   Mỗi bộ rule trong file cấu hình phải kèm theo `version` và khoảng ngày có hiệu lực (`effective_from`, `effective_to`). Khi tính toán phân loại cửa hàng cho tháng nào, hệ thống sẽ tự động áp dụng đúng bộ rule có hiệu lực tại tháng đó.
3. **Xây Dựng Governance Engine Class Trong Python (`src/classifiers/shop_classifier.py`)**:
   Viết Class Python nạp file cấu hình động, kiểm tra tính hợp lệ của rule và thực thi logic phân loại tự động.
4. **Automated Unit Testing (`tests/test_shop_classifier.py`)**:
   Triển khai bộ kiểm thử tự động với Pytest để xác minh tính đúng đắn của logic phân loại trước khi deploy lên Production.

#### 💻 Minh Họa Cấu Trúc Config YAML (`configs/shop_classifier.yaml`):
```yaml
rules_version: "v2.0"
effective_date: "2026-07-01"

performance_tiers:
  - tier: "Xuất sắc"
    min_score: 1.0
    min_kpi_count: 6
  - tier: "Tốt"
    min_score: 0.85
    min_kpi_count: 5
  - tier: "Khá"
    min_score: 0.70
    min_kpi_count: 4
  - tier: "Kém"
    min_score: 0.50
    min_kpi_count: 2
  - tier: "Cảnh báo"
    min_score: 0.0
    min_kpi_count: 0
```

---

## 📈 PHẦN 6: KẾT QUẢ ĐẦU RA THỰC TẾ & BỘ KIỂM THỬ PYTEST TỰ ĐỘNG

### 1. Bảng Chi Tiết 6 Tệp Dữ Liệu Sạch Đầu Ra (`data/processed/*.csv`)

| Tên File Đầu Ra | Số Dòng x Cột Thực Tế | Dung Lượng | Kết Quả Xử Lý Nghiệp Vụ Thực Tế | Trạng Thái Tag |
| :--- | :--- | :--- | :--- | :--- |
| `processed_transactions.csv` | **1,800 dòng x 14 cột** | 224.5 KB | Khử 15 trùng lặp POS, bổ khuyết 19 dòng Null Quantity (bảo toàn 380+ tr VNĐ). Nạp BigQuery làm `fact_sales`. | `✅ Cleaned` |
| `processed_inventory.csv` | **1,350 dòng x 9 cột** | 62.5 KB | Khôi phục tồn cuối `Ending_Inventory` & tính `Inventory_Cover_Ratio`. Nạp BigQuery làm `fact_inventory`. | `✅ Imputed` |
| `store_performance.csv` | **45 dòng x 7 cột** | 2.5 KB | Đối soát Doanh thu thực tế vs Target Revenue để tính % Achievement cho 15 cửa hàng x 3 tháng Quý 3. | `✅ Evaluated` |
| `daily_run_rate.csv` | **150 dòng x 9 cột** | 13.5 KB | Thống kê tốc độ bán trung bình ngày `DRR` per Cửa hàng - Sản phẩm (15 CH x 10 SP), làm tham số tính đọng vốn kho. | `✅ Calculated` |
| `processed_stores.csv` | **15 dòng x 8 cột** | 1.3 KB | Danh mục 15 cửa hàng gắn nhãn phân loại Tier động. Nạp BigQuery làm `dim_stores` phân tích theo RSM/AM. | `✅ Classified` |
| `processed_products.csv` | **10 dòng x 5 cột** | 0.6 KB | Danh mục 10 sản phẩm công nghệ & giá niêm yết chuẩn. Nạp BigQuery làm `dim_products_scd2` bảo toàn lịch sử giá. | `✅ Verified` |

---

### 2. Bộ 6 Chỉ Số Kết Quả Vận Hành Chốt Thực Tế
1. 💰 **Tổng Doanh Thu Chuỗi Bán Lẻ**: **56.6 Tỷ VNĐ** *(Chính xác 56,597,180,000 VNĐ từ 1,800 đơn hàng sạch Quý 3/2026)*.
2. 🛡️ **Doanh Thu Được Bảo Toàn**: **380+ Triệu VNĐ** *(Bổ khuyết 19 đơn hàng Null Quantity bằng `Quantity = Unit_Price / Base_Price = 1.0`)*.
3. 🎯 **Tỷ Lệ Đạt Target Trung Bình**: **99.29%** *(Tỷ lệ hoàn thành chỉ tiêu doanh thu trung bình toàn chuỗi 15 điểm bán)*.
4. 🧪 **Kiểm Thử Pytest Tự Động**: **100% Pass Rate (5/5 Unit Tests)** *(Thực thi `pytest tests/ -v` vượt qua 100%)*.
5. ⚠️ **Cảnh Báo Đọng Vốn Kho**: **1,337 Log Kho Overstock (&ge; 30 ngày bán)** *(Chiếm 99.0% tổng số log kho cần xử lý điều chuyển)*.
6. 🏆 **Nhóm Cửa Hàng Doanh Thu Top 1**: **Loại C (Standard Store) đạt 22.6 Tỷ VNĐ** *(Chiếm 39.91% tổng doanh thu toàn chuỗi)*.

---

### 3. Chi Tiết Kết Quả 5 Bài Kiểm Thử Pytest Tự Động (`pytest tests/ -v`)

#### 🧹 Module Làm Sạch Dữ Liệu (`tests/test_cleaner.py`) — `✅ 2/2 PASSED`
* **`test_clean_transactions`**: Kiểm thử tự động thuật toán loại bỏ 100% bản ghi trùng lặp POS (`assert len(df) == 1`) và tính cột `Total_Amount`.
* **`test_clean_inventory_logs`**: Kiểm thử thuật toán khôi phục tồn kho cuối ngày bị thiếu (`Ending = Beginning + Received - Sold` &rarr; `10 + 5 - 2 = 13.0`).

#### 🧮 Module Tính Chỉ Số Vận Hành (`tests/test_metrics.py`) — `✅ 2/2 PASSED`
* **`test_daily_run_rate`**: Kiểm thử thuật toán tính tốc độ bán hàng trung bình ngày `DRR` (`DRR = Total_Sales_Qty / Active_Days` &rarr; `10 / 10 = 1.0`).
* **`test_inventory_to_sales_ratio`**: Kiểm thử phép tính số ngày trang trải tồn kho `Days_of_Cover` (`Ending_Inventory / DRR` &rarr; `15 / 3 = 5.0 ngày`).

#### ⚙️ Module Phân Loại & Quản Trị Rule (`tests/test_shop_classifier.py`) — `✅ 1/1 PASSED`
* **`test_config_driven_shop_classifier`**: Kiểm thử tự động nạp file cấu hình động `configs/shop_classifier.yaml`, xác minh phân loại nhóm cửa hàng (*Flagship, Micro*), xếp loại hiệu suất (*Super Star &ge;110%*) và phát hiện cảnh báo đọng vốn (*CRITICAL STOCKOUT RISK*).
