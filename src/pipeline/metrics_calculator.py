import pandas as pd
import numpy as np
from src.utils.logger import setup_logger

logger = setup_logger("metrics_calculator")

class MetricsCalculator:
    """Calculates Daily Run Rate, Inventory to Sales Ratio, and Target Achievement."""

    @staticmethod
    def calculate_daily_run_rate(sales_df: pd.DataFrame, group_cols: list = ["Store_ID", "Product_ID"]) -> pd.DataFrame:
        """
        Calculates Daily Run Rate (DRR) for given grouping.
        DRR = Total Sales Quantity / Passed Days in the Period.
        """
        logger.info("Calculating Daily Run Rate (DRR)...")
        if sales_df.empty:
            return pd.DataFrame(columns=group_cols + ["Total_Sales_Qty", "Active_Days", "Daily_Run_Rate"])

        df = sales_df.copy()
        df["Date"] = pd.to_datetime(df["Date"])

        # Determine date range span per group or globally
        aggregated = df.groupby(group_cols).agg(
            Total_Sales_Qty=("Quantity", "sum"),
            Total_Sales_Amount=("Total_Amount", "sum"),
            Min_Date=("Date", "min"),
            Max_Date=("Date", "max"),
            Active_Days=("Date", lambda x: (x.max() - x.min()).days + 1)
        ).reset_index()

        # Ensure Active_Days is at least 1 to avoid division by zero
        aggregated["Active_Days"] = aggregated["Active_Days"].clip(lower=1)
        
        # Calculate Daily Run Rate (Quantity per day)
        aggregated["Daily_Run_Rate"] = aggregated["Total_Sales_Qty"] / aggregated["Active_Days"]
        
        # Calculate Daily Revenue Run Rate (Amount per day)
        aggregated["Daily_Revenue_Run_Rate"] = aggregated["Total_Sales_Amount"] / aggregated["Active_Days"]

        logger.info(f"Calculated Daily Run Rate for {len(aggregated)} records.")
        return aggregated

    @staticmethod
    def calculate_inventory_to_sales_ratio(
        inventory_df: pd.DataFrame, 
        drr_df: pd.DataFrame, 
        join_cols: list = ["Store_ID", "Product_ID"]
    ) -> pd.DataFrame:
        """
        Calculates Inventory to Sales Ratio (Days of Inventory Cover).
        Inventory_to_Sales_Ratio = Ending_Inventory / Daily_Run_Rate.
        """
        logger.info("Calculating Inventory-to-Sales Ratio...")
        if inventory_df.empty:
            return inventory_df

        merged = pd.merge(inventory_df, drr_df[join_cols + ["Daily_Run_Rate"]], on=join_cols, how="left")
        merged["Daily_Run_Rate"] = merged["Daily_Run_Rate"].fillna(0)

        # Calculate ratio safely
        merged["Inventory_to_Sales_Ratio"] = np.where(
            merged["Daily_Run_Rate"] > 0,
            merged["Ending_Inventory"] / merged["Daily_Run_Rate"],
            999.0 # High value indicating no sales / stagnant inventory
        )
        
        # Rounded for presentation
        merged["Inventory_to_Sales_Ratio"] = merged["Inventory_to_Sales_Ratio"].round(2)
        merged["Daily_Run_Rate"] = merged["Daily_Run_Rate"].round(2)
        
        logger.info(f"Calculated Inventory-to-Sales Ratio for {len(merged)} records.")
        return merged
