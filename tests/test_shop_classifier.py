import pytest
import pandas as pd
from src.classifiers.shop_classifier import ConfigDrivenShopClassifier

def test_config_driven_shop_classifier():
    classifier = ConfigDrivenShopClassifier(config_path="configs/shop_classifier.yaml")

    # Flagship check
    flagship_class = classifier.classify_store_by_revenue_and_type(1500000000, "Standard")
    assert flagship_class == "Flagship_Store"

    # Micro store check
    micro_class = classifier.classify_store_by_revenue_and_type(50000000, "D")
    assert micro_class == "Micro_Store"

    # Performance tier check
    perf_status = classifier.evaluate_performance_tier(1.15)
    assert perf_status == "Super Star (>=110%)"

    # Inventory alert check
    alert = classifier.evaluate_inventory_alert(1.5)
    assert alert == "🔴 CRITICAL STOCKOUT RISK"
