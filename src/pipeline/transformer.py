import pandas as pd
from typing import Dict, Tuple
from src.utils.logger import setup_logger
from src.pipeline.metrics_calculator import MetricsCalculator
from src.classifiers.shop_classifier import ConfigDrivenShopClassifier

logger = setup_logger("transformer")

class DataTransformer:
    """Transforms cleaned data tables and enriches them with derived metrics."""

    def __init__(self, classifier_config_path: str = "configs/shop_classifier.yaml"):
        self.classifier = ConfigDrivenShopClassifier(config_path=classifier_config_path)

    def transform_all(
        self, 
        cleaned_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.DataFrame]:
        """
        Executes end-to-end data transformation.
        
        Args:
            cleaned_data: Dict containing 'transactions', 'inventory_logs', 'store_info', 'products', 'targets'
            
        Returns:
            Dict containing transformed & enriched DataFrames.
        """
        logger.info("Starting Data Transformation Phase...")
        txns = cleaned_data["transactions"]
        inv = cleaned_data["inventory_logs"]
        stores = cleaned_data["store_info"]
        products = cleaned_data["products"]
        targets = cleaned_data["targets"]

        # 1. Calculate Daily Run Rate (DRR) per Store & Product
        drr_df = MetricsCalculator.calculate_daily_run_rate(txns, group_cols=["Store_ID", "Product_ID"])

        # 2. Enrich Inventory Logs with Inventory-to-Sales Ratio
        enriched_inv = MetricsCalculator.calculate_inventory_to_sales_ratio(inv, drr_df)

        # 3. Aggregate Monthly Revenue per Store for Classification & Target Achievement
        txns["Month_Year"] = txns["Date"].dt.to_period("M").astype(str)
        store_monthly_sales = txns.groupby(["Store_ID", "Month_Year"]).agg(
            Actual_Revenue=("Total_Amount", "sum"),
            Total_Orders=("Transaction_ID", "nunique"),
            Total_Items_Sold=("Quantity", "sum")
        ).reset_index()

        # Merge Target Revenue
        store_performance = pd.merge(
            store_monthly_sales, 
            targets, 
            on=["Store_ID", "Month_Year"], 
            how="left"
        )
        store_performance["Target_Revenue"] = store_performance["Target_Revenue"].fillna(0)
        
        # Calculate Achievement %
        store_performance["Achievement_Pct"] = np_safe_divide(
            store_performance["Actual_Revenue"], 
            store_performance["Target_Revenue"]
        )

        # 4. Apply Dynamic Config-driven Shop Classification & Performance Tiers
        classified_stores = self.classifier.classify_stores(stores, store_performance)

        # 5. Enrich Sales Transactions with Store & Product details
        enriched_txns = pd.merge(txns, stores[["Store_ID", "Store_Name", "Region", "Store_Type"]], on="Store_ID", how="left")
        enriched_txns = pd.merge(enriched_txns, products[["Product_ID", "Product_Name", "Brand", "Category"]], on="Product_ID", how="left")

        logger.info("Data Transformation completed successfully.")
        return {
            "processed_transactions": enriched_txns,
            "processed_inventory": enriched_inv,
            "processed_stores": classified_stores,
            "store_performance": store_performance,
            "processed_products": products,
            "daily_run_rate": drr_df
        }

def np_safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Safe division returning 0 on zero denominator."""
    return (numerator / denominator.replace(0, pd.NA)).fillna(0).round(4)
