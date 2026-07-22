import pandas as pd
from typing import Dict, Any, List
from src.utils.config_loader import load_yaml_config
from src.utils.logger import setup_logger

logger = setup_logger("shop_classifier")

class ConfigDrivenShopClassifier:
    """
    Refactored Governance Engine: Classifies stores dynamically based on 
    YAML configuration rules instead of hardcoded IF-ELSE branches.
    """

    def __init__(self, config_path: str = "configs/shop_classifier.yaml"):
        self.config_path = config_path
        self.config = load_yaml_config(config_path)
        self.rules = self.config.get("shop_classification_rules", {}).get("rules", [])
        self.perf_thresholds = self.config.get("performance_tier_rules", {}).get("target_achievement_thresholds", {})
        self.inventory_rules = self.config.get("inventory_alert_rules", {}).get("ratio_thresholds", {})
        logger.info(f"Loaded ConfigDrivenShopClassifier with {len(self.rules)} rules from {config_path}")

    def classify_store_by_revenue_and_type(self, avg_monthly_revenue: float, store_type: str) -> str:
        """Evaluates YAML rules top-to-bottom to assign store classification."""
        for rule in sorted(self.rules, key=lambda x: x.get("tier", 99)):
            conditions = rule.get("conditions", {})
            min_rev = conditions.get("min_monthly_revenue", 0)
            valid_types = conditions.get("store_types", [])

            if avg_monthly_revenue >= min_rev or store_type in valid_types:
                return rule.get("classification", "Standard_Store")

        return "Micro_Store"

    def evaluate_performance_tier(self, achievement_pct: float) -> str:
        """Evaluates target achievement percentage into performance status."""
        if achievement_pct >= self.perf_thresholds.get("super_star", 1.10):
            return "Super Star (>=110%)"
        elif achievement_pct >= self.perf_thresholds.get("on_track", 0.90):
            return "On Track (90-109%)"
        elif achievement_pct >= self.perf_thresholds.get("underperforming", 0.70):
            return "Underperforming (70-89%)"
        else:
            return "Critical Warning (<70%)"

    def evaluate_inventory_alert(self, inventory_ratio: float) -> str:
        """Evaluates Inventory-to-Sales Ratio into actionable operational alert."""
        if inventory_ratio <= self.inventory_rules.get("critical_stockout", 2.0):
            return "🔴 CRITICAL STOCKOUT RISK"
        elif inventory_ratio <= self.inventory_rules.get("low_inventory", 5.0):
            return "🟡 LOW INVENTORY WARNING"
        elif inventory_ratio <= self.inventory_rules.get("optimal", 15.0):
            return "🟢 OPTIMAL STOCK LEVEL"
        else:
            return "🔵 OVERSTOCK RISK"

    def classify_stores(self, store_info_df: pd.DataFrame, performance_df: pd.DataFrame) -> pd.DataFrame:
        """
        Classifies all stores in the DataFrame based on historical revenue and metadata.
        """
        df = store_info_df.copy()

        # Calculate average monthly revenue per store
        avg_rev = performance_df.groupby("Store_ID")["Actual_Revenue"].mean().reset_index()
        avg_rev.rename(columns={"Actual_Revenue": "Avg_Monthly_Revenue"}, inplace=True)

        df = pd.merge(df, avg_rev, on="Store_ID", how="left")
        df["Avg_Monthly_Revenue"] = df["Avg_Monthly_Revenue"].fillna(0)

        # Apply classification
        df["Dynamic_Classification"] = df.apply(
            lambda row: self.classify_store_by_revenue_and_type(row["Avg_Monthly_Revenue"], row["Store_Type"]),
            axis=1
        )

        logger.info(f"Classified {len(df)} stores using YAML Rule Engine.")
        return df
