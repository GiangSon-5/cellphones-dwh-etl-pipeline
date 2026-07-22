import pandas as pd
from typing import List, Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger("validators")

def validate_columns(df: pd.DataFrame, required_columns: List[str], df_name: str) -> bool:
    """Validates that a DataFrame contains all required columns."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error(f"[{df_name}] Missing required columns: {missing}")
        raise ValueError(f"[{df_name}] Missing required columns: {missing}")
    logger.info(f"[{df_name}] Column validation passed ({len(required_columns)} columns verified).")
    return True

def validate_non_negative_numeric(df: pd.DataFrame, numeric_columns: List[str], df_name: str) -> pd.DataFrame:
    """Ensures specified numeric columns contain non-negative numbers."""
    df_clean = df.copy()
    for col in numeric_columns:
        if col in df_clean.columns:
            negative_count = (df_clean[col] < 0).sum()
            if negative_count > 0:
                logger.warning(f"[{df_name}] Found {negative_count} negative values in {col}. Clipping to 0.")
                df_clean[col] = df_clean[col].clip(lower=0)
    return df_clean
