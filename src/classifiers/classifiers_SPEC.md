# Đặc tả Kỹ thuật Module Classifiers (SPEC)

## 1. Tổng quan Module
Module `src/classifiers` đóng vai trò là Refactored Config-Driven Governance Engine. Thay vì hardcode các điều kiện `if-else` trong mã nguồn Python khi phân loại 170+ cửa hàng CellphoneS, engine đọc cấu hình từ file `configs/shop_classifier.yaml`.

## 2. Kiến trúc & Design Patterns
- **Pattern**: Strategy & Policy Pattern (Driven by Config File).
- **Class thực thi**: `ConfigDrivenShopClassifier` (`src/classifiers/shop_classifier.py`).

### 2.1 Các Phương thức Interface
- `__init__(config_path: str)`: Khởi tạo engine và load các quy tắc từ YAML.
- `classify_store_by_revenue_and_type(avg_monthly_revenue: float, store_type: str) -> str`: Đánh giá danh mục cửa hàng (`Flagship_Store`, `Key_Store`, `Standard_Store`, `Micro_Store`).
- `evaluate_performance_tier(achievement_pct: float) -> str`: Phân hạng hiệu năng kinh doanh (`Super Star`, `On Track`, `Underperforming`, `Critical Warning`).
- `evaluate_inventory_alert(inventory_ratio: float) -> str`: Đánh giá trạng thái tồn kho (`CRITICAL STOCKOUT RISK`, `LOW INVENTORY WARNING`, `OPTIMAL STOCK LEVEL`, `OVERSTOCK RISK`).

## 3. Mở rộng & Bảo trì (Maintenance)
Khi ban quản trị CellphoneS thay đổi ngưỡng doanh thu cửa hàng Flagship từ 1.2 tỷ lên 1.5 tỷ VND, Analytics Engineer chỉ cần cập nhật file `configs/shop_classifier.yaml` mà **không cần sửa đổi bất kỳ dòng code Python nào** hay deploy lại package core.
