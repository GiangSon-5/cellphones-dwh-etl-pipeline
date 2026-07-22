import pytest
import pandas as pd
from src.pipeline.metrics_calculator import MetricsCalculator

def test_daily_run_rate():
    sales_data = pd.DataFrame({
        "Store_ID": ["ST001", "ST001", "ST001"],
        "Product_ID": ["P001", "P001", "P001"],
        "Date": ["2026-07-01", "2026-07-02", "2026-07-10"],
        "Quantity": [2, 3, 5],
        "Total_Amount": [200, 300, 500]
    })

    drr_df = MetricsCalculator.calculate_daily_run_rate(sales_data)
    assert len(drr_df) == 1
    # Active days: 2026-07-01 to 2026-07-10 = 10 days
    # Total Qty = 10 -> DRR = 10 / 10 = 1.0
    assert drr_df["Daily_Run_Rate"].iloc[0] == 1.0

def test_inventory_to_sales_ratio():
    inv_df = pd.DataFrame({
        "Store_ID": ["ST001"],
        "Product_ID": ["P001"],
        "Ending_Inventory": [15.0]
    })
    drr_df = pd.DataFrame({
        "Store_ID": ["ST001"],
        "Product_ID": ["P001"],
        "Daily_Run_Rate": [3.0]
    })

    result = MetricsCalculator.calculate_inventory_to_sales_ratio(inv_df, drr_df)
    # Ratio = 15 / 3 = 5.0 days
    assert result["Inventory_to_Sales_Ratio"].iloc[0] == 5.0
