# Báo Cáo  - Hệ Thống Data Warehouse & Analytics Pipeline CellphoneS (170+ Cửa hàng)

🌐 **[Xem Bản Trình Báo Cáo Web Portal Trực Tuyến (Vercel Production)](https://cellphones-dwh-etl-pipeline.vercel.app/)** | 📄 **[Xem Tệp Báo Cáo Tổng Hợp Chi Tiết (PROJECT_REPORT.md)](PROJECT_REPORT.md)**

---

[![Live Web Portal](https://img.shields.io/badge/Live_Web_Portal-Vercel_App-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://cellphones-dwh-etl-pipeline.vercel.app/)
[![Python ETL](https://img.shields.io/badge/ETL_Pipeline-Python_Pandas-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://cellphones-dwh-etl-pipeline.vercel.app/)
[![Power BI](https://img.shields.io/badge/Dashboard-Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://cellphones-dwh-etl-pipeline.vercel.app/)

![Cellphones Power BI Operational Dashboard](assets/images/power%20bi.png)
![Cellphones Data Warehouse ERD Star Schema](assets/images/ERD.png)

---

## 📌 Tổng Quan Dự Án
Hệ thống **End-to-End Data Warehouse & Analytics Pipeline** phục vụ Chuỗi Bán lẻ Điện thoại & Thiết bị Công nghệ CellphoneS (170+ cửa hàng). Dự án được triển khai từ con số 0 (From Scratch) đáp ứng trọn vẹn yêu cầu kiểm tra kỹ thuật Analytics Engineer 48h.

Hệ thống tiếp nhận 5 luồng dữ liệu thô (Transactions, Inventory Logs, Store Info, Products, Targets), tự động hóa quy trình **Data Cleaning & Transformation**, tính toán các chỉ số vận hành cốt lõi (**Daily Run Rate**, **Inventory Cover Ratio**), triển khai kiến trúc **SCD Type 2** trên BigQuery, thiết lập mô hình **Power BI Semantic Model (DAX Virtual Tables)**, và xây dựng **Config-Driven Governance Engine** quản trị phân loại cửa hàng linh hoạt.

---

## 📑 BÁO CÁO TOÀN DIỆN & BẢN TRÌNH BÀY (LIÊN KẾT ĐỌC BÁO CÁO)

Dự án cung cấp 2 phương thức theo dõi báo cáo đánh giá chuyên sâu dành cho nhà tuyển dụng và các kỹ sư dữ liệu:

* 🌐 **[BẢN LIVE WEB PORTAL (Vercel Production App)](https://cellphones-dwh-etl-pipeline.vercel.app/)**: Giao diện Web Portal hiện đại 5 Tab tương tác trực tuyến, tích hợp đầy đủ sơ đồ Mermaid, trực quan hóa Dashboard Power BI, 5 ví dụ tối ưu SQL, bộ 6 file dữ liệu sạch đầu ra (xem trước mẫu 5 dòng với nút Toggle) và báo cáo 5 bài Pytest Unit tests.
* 📄 **[BÁO CÁO TỔNG HỢP CHI TIẾT (PROJECT_REPORT.md)](PROJECT_REPORT.md)**: File tài liệu Markdown tổng hợp duy nhất chứa toàn bộ nội dung thuyết minh kỹ thuật, sơ đồ Data Warehouse 3 tầng, công thức DAX Virtual Tables (Input/Output Specs), quy trình điều tra sự cố BigQuery và bộ chỉ số kết quả thực tế.

---

## 📓 Danh sách 6 File Jupyter Notebook EDA Chuyên nghiệp (`notebooks/`)

| File Notebook | Mục tiêu Phân tích & Thực nghiệm Dữ liệu |
| :--- | :--- |
| 📓 [eda_01_transactions.ipynb](notebooks/eda_01_transactions.ipynb) | Phân tích chuyên sâu giao dịch bán hàng, kiểm tra trùng lặp `Transaction_ID`, doanh thu daily/monthly, sản phẩm bán chạy. |
| 📓 [eda_02_inventory_logs.ipynb](notebooks/eda_02_inventory_logs.ipynb) | Phân tích nhật ký tồn kho daily, kiểm định công thức xuất nhập tồn (`Beginning + Received - Sold = Ending`) & cảnh báo cháy hàng. |
| 📓 [eda_03_store_info.ipynb](notebooks/eda_03_store_info.ipynb) | Phân tích master cửa hàng, phân bổ loại hình cửa hàng (A, B, C, D), khu vực (Region) & bộ máy quản lý (RSM/AM). |
| 📓 [eda_04_products.ipynb](notebooks/eda_04_products.ipynb) | Phân tích danh mục sản phẩm master, cơ cấu thương hiệu (Brand), danh mục (Category) & dải giá niêm yết (Base Price). |
| 📓 [eda_05_targets.ipynb](notebooks/eda_05_targets.ipynb) | Phân tích chỉ tiêu doanh thu Target hàng tháng của từng cửa hàng. |
| 📓 [eda_06_integrated_analytics.ipynb](notebooks/eda_06_integrated_analytics.ipynb) | **Notebook EDA Tích hợp 5 Datasets**: Tính toán `Daily_Run_Rate`, `Inventory_to_Sales_Ratio`, `% Target Achievement` & biểu đồ Dashboard. |

---

## 🗺️ Bảng Ánh Xạ Yêu Cầu Đánh Giá (Assessment Requirement Mapping)

| Phần Đề bài Test AE 48h | Tóm tắt Giải pháp Engineering | File Code & Tài liệu Chi tiết (Liên kết mở trực tiếp) |
| :--- | :--- | :--- |
| **PHẦN 1: Mô hình hóa Data Warehouse & SCD Type 2** | • Thiết kế Data Warehouse 3 Tầng (Staging - Intermediate - Marts).<br>• Sơ đồ ERD Star Schema nằm tại **Tầng Marts (`marts_*`)** & SCD Type 2 tại **Tầng Intermediate**.<br>• BigQuery DDL/DML MERGE Pattern (`product_sk`, `valid_from`, `valid_to`, `is_current`). | 📄 [Báo cáo Chi tiết Phần 1](PROJECT_REPORT.md#phần-2-kiến-trúc-data-warehouse-scd-type-2--python-etl-pipeline)<br>📄 [BigQuery DDL SCD2 Products](models/intermediate/dim_products_scd2.sql)<br>📄 [BigQuery Fact Sales SQL](models/marts/fact_sales.sql)<br>📄 [BigQuery Fact Inventory SQL](models/marts/fact_inventory_daily.sql) |
| **PHẦN 2: Data Pipeline ETL & Tính toán Chỉ số** | • Module Python ETL (Clean, Transform, Metrics, Export).<br>• Tính toán `Daily_Run_Rate` = `Sales_Qty` / `Active_Days`.<br>• Tính toán `Inventory_to_Sales_Ratio` = `Ending_Inventory` / `DRR`.<br>• Xuất dữ liệu sạch ra `data/processed/*.csv`. | 🐍 [Module Làm sạch Dữ liệu](src/pipeline/cleaner.py)<br>🐍 [Module Tính toán Chỉ số Metrics](src/pipeline/metrics_calculator.py)<br>🐍 [Module Biến đổi Dữ liệu Transformer](src/pipeline/transformer.py)<br>🐍 [Script Thực thi Runner](src/pipeline/runner.py)<br>📊 [Thư mục Dữ liệu Đầu ra](data/processed) |
| **PHẦN 3: Power BI Semantic Model & Mã DAX** | • Mô hình Star Schema cho Power BI (Quan hệ 1-nhiều).<br>• DAX Measures (Total Revenue, Target %, DRR, Alert Flags).<br>• DAX Virtual Tables (`vtable_StoreTypeRevenueAllocation`, `vtable_StoreTargetAchievement`). | 📈 [Mã nguồn DAX Measures](powerbi/dax_measures.dax)<br>📈 [Mã nguồn DAX Virtual Tables](powerbi/virtual_tables.dax)<br>📄 [Báo cáo Chi tiết Phần 3 (DAX Specs)](PROJECT_REPORT.md#-phần-3-power-bi-operational-dashboard--dax-virtual-tables)<br>📊 [File Power BI Dashboard (.pbix)](powerbi/Cellphones_Operational_Dashboard.pbix) |
| **PHẦN 4: Refactoring Governance & Tối ưu BigQuery** | • Tách biệt logic nghiệp vụ sang Config-Driven Rule Engine (`configs/shop_classifier.yaml`).<br>• Class Python phân loại 170+ cửa hàng linh hoạt.<br>• Tài liệu Hướng dẫn Xử lý Sự cố & Tối ưu Chi phí BigQuery (5 ví dụ SQL 1-1). | ⚙️ [Cấu hình Quy tắc Rule Engine YAML](configs/shop_classifier.yaml)<br>🐍 [Mã nguồn Classifier Engine](src/classifiers/shop_classifier.py)<br>📄 [Báo cáo Chi tiết Phần 4 (Tối ưu BQ)](PROJECT_REPORT.md#-phần-4-tư-duy-hệ-thống---điều-tra-chi-phí-bigquery--refactored-codebase) |

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

---

🌐 **[Live Web Presentation Portal (Vercel)](https://cellphones-dwh-etl-pipeline.vercel.app/)** | 📄 **[Tệp Báo Cáo Chi Tiết (PROJECT_REPORT.md)](PROJECT_REPORT.md)**
