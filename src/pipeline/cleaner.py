import pandas as pd
import numpy as np
from typing import Dict
from src.utils.logger import setup_logger
from src.utils.validators import validate_columns, validate_non_negative_numeric

logger = setup_logger("cleaner")

class DataCleaner:
    """Handles loading, cleaning, deduplication, and type validation for raw data inputs."""

    def __init__(self, raw_data_dir: str):
        self.raw_data_dir = raw_data_dir

    def clean_transactions(self, file_name: str = "Transactions.csv") -> pd.DataFrame:
        """Cleans transactions data."""
        file_path = f"{self.raw_data_dir}/{file_name}"
        logger.info(f"Loading Transactions from {file_path}...")
        df = pd.read_csv(file_path)
        
        required_cols = ["Transaction_ID", "Date", "Product_ID", "Store_ID", "Quantity", "Unit_Price"]
        validate_columns(df, required_cols, "Transactions")

        # Clean duplicates
        init_len = len(df)
        df = df.drop_duplicates(subset=["Transaction_ID"])
        logger.info(f"[Transactions] Deduplicated {init_len - len(df)} duplicate Transaction_IDs.")

        # Cast Date safely handling mixed formats like DD/MM/YYYY or YYYY-MM-DD
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="mixed", errors="coerce")
        df = df.dropna(subset=["Date"])

        # Cast Numeric & Fill Nulls with Unit_Price / Base_Price ratio imputation matching eda_01_transactions.ipynb
        df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce").fillna(0)
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

        if "Base_Price" in df.columns:
            imputed_qty = (df["Unit_Price"] / df["Base_Price"]).round().fillna(1.0)
            df["Quantity"] = np.where(df["Quantity"].isna() | (df["Quantity"] <= 0), imputed_qty, df["Quantity"])
        else:
            try:
                prod_path = f"{self.raw_data_dir}/Products.csv"
                df_prod = pd.read_csv(prod_path)
                df_m = pd.merge(df, df_prod[["Product_ID", "Base_Price"]], on="Product_ID", how="left")
                imputed_qty = (df_m["Unit_Price"] / df_m["Base_Price"]).round().fillna(1.0)
                df["Quantity"] = np.where(df["Quantity"].isna() | (df["Quantity"] <= 0), imputed_qty, df["Quantity"])
            except Exception:
                df["Quantity"] = df["Quantity"].fillna(1.0)

        df["Quantity"] = df["Quantity"].clip(lower=1)
        df = validate_non_negative_numeric(df, ["Quantity", "Unit_Price"], "Transactions")

        # Calculate Total Amount
        df["Total_Amount"] = df["Quantity"] * df["Unit_Price"]
        return df

    def clean_inventory_logs(self, file_name: str = "Inventory_Logs.csv") -> pd.DataFrame:
        """Cleans inventory logs data."""
        file_path = f"{self.raw_data_dir}/{file_name}"
        logger.info(f"Loading Inventory Logs from {file_path}...")
        df = pd.read_csv(file_path)

        required_cols = ["Log_Date", "Store_ID", "Product_ID", "Beginning_Inventory", "Received", "Sold", "Ending_Inventory"]
        validate_columns(df, required_cols, "Inventory_Logs")

        # Cast Log_Date safely
        df["Log_Date"] = pd.to_datetime(df["Log_Date"], dayfirst=True, format="mixed", errors="coerce")
        df = df.dropna(subset=["Log_Date"])

        # Numeric conversions
        num_cols = ["Beginning_Inventory", "Received", "Sold", "Ending_Inventory"]
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        
        df = validate_non_negative_numeric(df, num_cols, "Inventory_Logs")

        # Fix/Recompute Ending_Inventory if missing or inconsistent: Beginning + Received - Sold
        calculated_ending = df["Beginning_Inventory"] + df["Received"] - df["Sold"]
        df["Ending_Inventory"] = np.where(
            df["Ending_Inventory"].isna() | (df["Ending_Inventory"] == 0),
            calculated_ending,
            df["Ending_Inventory"]
        )
        df["Ending_Inventory"] = df["Ending_Inventory"].clip(lower=0)

        # Deduplicate on (Log_Date, Store_ID, Product_ID)
        df = df.drop_duplicates(subset=["Log_Date", "Store_ID", "Product_ID"], keep="last")
        return df

    def clean_store_info(self, file_name: str = "Store_Info.csv") -> pd.DataFrame:
        """Cleans store information data."""
        file_path = f"{self.raw_data_dir}/{file_name}"
        logger.info(f"Loading Store Info from {file_path}...")
        df = pd.read_csv(file_path)

        required_cols = ["Store_ID", "Store_Name", "Region", "RSM", "AM", "Store_Type"]
        validate_columns(df, required_cols, "Store_Info")

        df = df.drop_duplicates(subset=["Store_ID"])
        df["Store_Name"] = df["Store_Name"].fillna("Unknown Store")
        df["Region"] = df["Region"].fillna("Miền Nam")
        df["Store_Type"] = df["Store_Type"].fillna("Standard")
        return df

    def clean_products(self, file_name: str = "Products.csv") -> pd.DataFrame:
        """Cleans products dimension data."""
        file_path = f"{self.raw_data_dir}/{file_name}"
        logger.info(f"Loading Products from {file_path}...")
        df = pd.read_csv(file_path)

        required_cols = ["Product_ID", "Product_Name", "Brand", "Category", "Base_Price"]
        validate_columns(df, required_cols, "Products")

        df = df.drop_duplicates(subset=["Product_ID"])
        df["Base_Price"] = pd.to_numeric(df["Base_Price"], errors="coerce").fillna(0)
        return df

    def clean_targets(self, file_name: str = "Targets.csv") -> pd.DataFrame:
        """Cleans targets data."""
        file_path = f"{self.raw_data_dir}/{file_name}"
        logger.info(f"Loading Targets from {file_path}...")
        df = pd.read_csv(file_path)

        required_cols = ["Store_ID", "Month_Year", "Target_Revenue"]
        validate_columns(df, required_cols, "Targets")

        df = df.drop_duplicates(subset=["Store_ID", "Month_Year"])
        df["Target_Revenue"] = pd.to_numeric(df["Target_Revenue"], errors="coerce").fillna(0)
        return df
