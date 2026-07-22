# Đặc tả Kỹ thuật Power BI Semantic Model (SPEC)

## 1. Cấu trúc Mô hình Dữ liệu (Semantic Model Topography)
Mô hình Semantic Model được thiết kế chuẩn theo kiến trúc Star Schema (Mô hình Ngôi sao):

```
                     +-------------------+
                     |     dim_store     |
                     +-------------------+
                       |               |
             1:N (1)   |               |   1:N (2)
                       v               v
             +-------------------+   +-----------------------+
             |    fact_sales     |   | fact_inventory_daily  |
             +-------------------+   +-----------------------+
                       ^
             1:N (3)   |
                       |
                     +-------------------+
                     |    dim_product    |
                     +-------------------+
```

## 2. Ma trận Ma trận DAX Measures

| Tên Measure | Công thức Nghiệp vụ | Mã DAX |
| :--- | :--- | :--- |
| **Total Revenue** | $\sum \text{total\_amount}$ | `SUM(fact_sales[total_amount])` |
| **Target Achievement %** | $\frac{\text{Actual Revenue}}{\text{Target Revenue}}$ | `DIVIDE([Total Sales Revenue], [Total Target Revenue], 0)` |
| **Daily Run Rate (DRR)** | $\text{Tốc độ bán trượt 30 ngày}$ | `AVERAGE(fact_inventory_daily[daily_run_rate])` |
| **Inventory to Sales Ratio** | $\frac{\text{Ending Inventory}}{\text{DRR}}$ | `AVERAGE(fact_inventory_daily[inventory_to_sales_ratio])` |
| **Stockout Risk Warning** | Nhãn Cảnh báo Cháy hàng | `IF([Inventory to Sales Ratio] <= 2.0, "🔴 CRITICAL STOCKOUT", "🟢 SAFE")` |

## 3. Logic Bảng ảo DAX (Virtual Tables)
Sử dụng các hàm `SUMMARIZE`, `ADDCOLUMNS`, `CALCULATE` và `ALL` để xây dựng bảng ảo phục vụ báo cáo ma trận phân bổ doanh thu (`vtable_RegionalRevenueAllocation`) và đánh giá tỷ lệ hoàn thành KPI cửa hàng (`vtable_StoreTargetAchievement`).
