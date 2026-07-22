import pytest
import pandas as pd
from src.pipeline.cleaner import DataCleaner

def test_clean_transactions(tmp_path):
    # Prepare dummy CSV
    d = tmp_path / "raw"
    d.mkdir()
    p = d / "Transactions.csv"
    p.write_text("Transaction_ID,Date,Product_ID,Store_ID,Quantity,Unit_Price\nTXN1,2026-07-01,P001,ST001,2,10000\nTXN1,2026-07-01,P001,ST001,2,10000\n", encoding="utf-8")

    cleaner = DataCleaner(raw_data_dir=str(d))
    df = cleaner.clean_transactions("Transactions.csv")

    # Assert deduplication
    assert len(df) == 1
    assert "Total_Amount" in df.columns
    assert df["Total_Amount"].iloc[0] == 20000

def test_clean_inventory_logs(tmp_path):
    d = tmp_path / "raw"
    d.mkdir()
    p = d / "Inventory_Logs.csv"
    p.write_text("Log_Date,Store_ID,Product_ID,Beginning_Inventory,Received,Sold,Ending_Inventory\n2026-07-01,ST001,P001,10,5,2,\n", encoding="utf-8")

    cleaner = DataCleaner(raw_data_dir=str(d))
    df = cleaner.clean_inventory_logs("Inventory_Logs.csv")

    # Assert Ending_Inventory calculated: 10 + 5 - 2 = 13
    assert df["Ending_Inventory"].iloc[0] == 13.0
