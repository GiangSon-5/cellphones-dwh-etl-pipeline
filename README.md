# Đánh giá Năng lực Analytics Engineer - Hệ thống Data Warehouse & Analytics Pipeline CellphoneS (170+ Cửa hàng)

## 📌 Tổng quan Hệ thống
Hệ thống **End-to-End Data Warehouse & Analytics Pipeline** phục vụ Chuỗi Bán lẻ Điện thoại CellphoneS (170+ cửa hàng). Dự án được khởi tạo từ con số 0 (From Scratch) tuân thủ nghiêm ngặt tiêu chuẩn **Production Software Architecture**.

Hệ thống xử lý 3 luồng dữ liệu thô (Transactions, Inventory Logs, Store Info, Products, Targets), thực thi Data Cleaning & Transformation, tính toán các chỉ số vận hành cốt lõi (**Daily Run Rate**, **Inventory-to-Sales Ratio**), triển khai **SCD Type 2 Architecture** trên BigQuery, mô hình hóa **Power BI Semantic Model (DAX Virtual Tables)**, và xây dựng **Config-Driven Governance Engine** phân loại cửa hàng linh hoạt.

---

## 📓 Danh sách 6 File Jupyter Notebook EDA Chuyên nghiệp (`notebooks/`)

| File Notebook | Mục tiêu Phân tích & Thực nghiệm Dữ liệu |
| :--- | :--- |
| 📓 [eda_01_transactions.ipynb](file:///C:/Users/Admin/Desktop/cellphones_test/notebooks/eda_01_transactions.ipynb) | Phân tích chuyên sâu giao dịch bán hàng, kiểm tra trùng lặp `Transaction_ID`, doanh thu daily/monthly, sản phẩm bán chạy. |
| 📓 [eda_02_inventory_logs.ipynb](file:///C:/Users/Admin/Desktop/cellphones_test/notebooks/eda_02_inventory_logs.ipynb) | Phân tích nhật ký tồn kho daily, kiểm định công thức xuất nhập tồn (`Beginning + Received - Sold = Ending`) & cảnh báo cháy hàng. |
| 📓 [eda_03_store_info.ipynb](file:///C:/Users/Admin/Desktop/cellphones_test/notebooks/eda_03_store_info.ipynb) | Phân tích master cửa hàng, phân bổ loại hình cửa hàng (A, B, C, D), khu vực (Region) & bộ máy quản lý (RSM/AM). |
| 📓 [eda_04_products.ipynb](file:///C:/Users/Admin/Desktop/cellphones_test/notebooks/eda_04_products.ipynb) | Phân tích danh mục sản phẩm master, cơ cấu thương hiệu (Brand), danh mục (Category) & dải giá niêm yết (Base Price). |
| 📓 [eda_05_targets.ipynb](file:///C:/Users/Admin/Desktop/cellphones_test/notebooks/eda_05_targets.ipynb) | Phân tích chỉ tiêu doanh thu Target hàng tháng của từng cửa hàng. |
| 📓 [eda_06_integrated_analytics.ipynb](file:///C:/Users/Admin/Desktop/cellphones_test/notebooks/eda_06_integrated_analytics.ipynb) | **Notebook EDA Tích hợp 5 Datasets**: Tính toán `Daily_Run_Rate`, `Inventory_to_Sales_Ratio`, `% Target Achievement` & biểu đồ Dashboard. |

---

## 🗺️ Bảng Ánh Xạ Yêu Cầu Đánh Giá (Assessment Requirement Mapping)

| Phần Đề bài Test AE 48h | Tóm tắt Giải pháp Engineering | File Code & Tài liệu Chi tiết (Liên kết mở trực tiếp) |
| :--- | :--- | :--- |
| **PHẦN 1: Mô hình hóa Data Warehouse & SCD Type 2** | • Thiết kế Data Warehouse 3 Tầng (Staging - Intermediate - Marts).<br>• Sơ đồ ERD Star Schema & Kiến trúc SCD Type 2 cho sản phẩm.<br>• BigQuery DDL/DML MERGE Pattern (`product_sk`, `valid_from`, `valid_to`, `is_current`). | 📄 [Tài liệu Kiến trúc ERD & SCD2](file:///C:/Users/Admin/Desktop/cellphones_test/docs/architecture/ERD_AND_SCD2_ARCHITECTURE.md)<br>📄 [BigQuery DDL SCD2 Products](file:///C:/Users/Admin/Desktop/cellphones_test/models/intermediate/dim_products_scd2.sql)<br>📄 [BigQuery Fact Sales SQL](file:///C:/Users/Admin/Desktop/cellphones_test/models/marts/fact_sales.sql)<br>📄 [BigQuery Fact Inventory SQL](file:///C:/Users/Admin/Desktop/cellphones_test/models/marts/fact_inventory_daily.sql) |
| **PHẦN 2: Data Pipeline ETL & Tính toán Chỉ số** | • Module Python ETL (Clean, Transform, Metrics, Export).<br>• Tính toán `Daily_Run_Rate` = `Sales_Qty` / `Active_Days`.<br>• Tính toán `Inventory_to_Sales_Ratio` = `Ending_Inventory` / `DRR`.<br>• Xuất dữ liệu sạch ra `data/processed/*.csv`. | 🐍 [Module Làm sạch Dữ liệu](file:///C:/Users/Admin/Desktop/cellphones_test/src/pipeline/cleaner.py)<br>🐍 [Module Tính toán Chỉ số Metrics](file:///C:/Users/Admin/Desktop/cellphones_test/src/pipeline/metrics_calculator.py)<br>🐍 [Module Biến đổi Dữ liệu Transformer](file:///C:/Users/Admin/Desktop/cellphones_test/src/pipeline/transformer.py)<br>🐍 [Script Thực thi Runner](file:///C:/Users/Admin/Desktop/cellphones_test/src/pipeline/runner.py)<br>📊 [Thư mục Dữ liệu Đầu ra](file:///C:/Users/Admin/Desktop/cellphones_test/data/processed) |
| **PHẦN 3: Power BI Semantic Model & Mã DAX** | • Mô hình Star Schema cho Power BI (Quan hệ 1-nhiều).<br>• DAX Measures (Total Revenue, Target %, DRR, Alert Flags).<br>• DAX Virtual Tables (`vtable_RegionalRevenueAllocation`, `vtable_StoreTargetAchievement`). | 📈 [Mã nguồn DAX Measures](file:///C:/Users/Admin/Desktop/cellphones_test/powerbi/dax_measures.dax)<br>📈 [Mã nguồn DAX Virtual Tables](file:///C:/Users/Admin/Desktop/cellphones_test/powerbi/virtual_tables.dax)<br>📄 [Đặc tả Power BI Semantic Model SPEC](file:///C:/Users/Admin/Desktop/cellphones_test/docs/powerbi_specs/POWERBI_SEMANTIC_MODEL_SPEC.md)<br>📄 [Tài liệu Power BI SRS](file:///C:/Users/Admin/Desktop/cellphones_test/docs/powerbi_specs/POWERBI_SEMANTIC_MODEL_SRS.md) |
| **PHẦN 4: Refactoring Governance & Tối ưu BigQuery** | • Tách biệt logic nghiệp vụ sang Config-Driven Rule Engine (`configs/shop_classifier.yaml`).<br>• Class Python phân loại 170+ cửa hàng linh hoạt.<br>• Tài liệu Hướng dẫn Xử lý Sự cố & Tối ưu Chi phí BigQuery (Partitioning, Clustering, BI Engine). | ⚙️ [Cấu hình Quy tắc Rule Engine YAML](file:///C:/Users/Admin/Desktop/cellphones_test/configs/shop_classifier.yaml)<br>🐍 [Mã nguồn Classifier Engine](file:///C:/Users/Admin/Desktop/cellphones_test/src/classifiers/shop_classifier.py)<br>📄 [Hướng dẫn Tối ưu & Xử lý Sự cố BigQuery](file:///C:/Users/Admin/Desktop/cellphones_test/docs/governance/BQ_COST_PERFORMANCE_TROUBLESHOOTING.md) |

---

## 🏗️ Cấu trúc & Bộ Tài liệu Module (`_SPEC.md` & `_SRS.md`)

Mỗi module chính trong hệ thống đều được trang bị bộ đôi tài liệu tiêu chuẩn:
- **`[module]_SPEC.md` (Đặc tả Kỹ thuật)**: Dành cho Analytics Engineer / Data Engineers.
- **`[module]_SRS.md` (Đặc tả Yêu cầu Nghiệp vụ)**: Dành cho Business Analyst / Product Owner.

---

## ⚡ Hướng dẫn Chạy & Kiểm tra Nhanh (Quickstart Guide)

### 1. Cài đặt Môi trường Python
```bash
pip install -r requirements.txt
```

### 2. Thực thi Data Pipeline ETL (Phần 2)
```bash
python -m src.pipeline.runner
```

### 3. Chạy Automated Unit Tests
```bash
python -m pytest tests/ -v
```
