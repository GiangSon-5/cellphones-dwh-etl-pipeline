import os
import pandas as pd
from src.utils.logger import setup_logger
from src.utils.config_loader import load_yaml_config
from src.pipeline.cleaner import DataCleaner
from src.pipeline.transformer import DataTransformer

logger = setup_logger("pipeline_runner")

def run_pipeline(config_path: str = "configs/pipeline_config.yaml") -> None:
    """Orchestrates full ETL pipeline execution."""
    logger.info("==================================================")
    logger.info("   CELLPHONES DATA PIPELINE ETL EXECUTION START   ")
    logger.info("==================================================")

    # 1. Load Configurations
    config = load_yaml_config(config_path)
    raw_dir = config["pipeline"]["raw_data_dir"]
    out_dir = config["pipeline"]["processed_data_dir"]
    os.makedirs(out_dir, exist_ok=True)

    # 2. Data Cleaning Phase
    cleaner = DataCleaner(raw_data_dir=raw_dir)
    cleaned_data = {
        "transactions": cleaner.clean_transactions(),
        "inventory_logs": cleaner.clean_inventory_logs(),
        "store_info": cleaner.clean_store_info(),
        "products": cleaner.clean_products(),
        "targets": cleaner.clean_targets()
    }

    # 3. Data Transformation Phase
    transformer = DataTransformer(classifier_config_path="configs/shop_classifier.yaml")
    transformed_data = transformer.transform_all(cleaned_data)

    # 4. Export Processed Data Outputs
    logger.info(f"Exporting processed CSV artifacts to '{out_dir}'...")
    for key, df in transformed_data.items():
        file_path = os.path.join(out_dir, f"{key}.csv")
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        logger.info(f"  -> Exported {key}.csv ({len(df)} rows, {len(df.columns)} cols) to {file_path}")

    logger.info("==================================================")
    logger.info("  CELLPHONES DATA PIPELINE COMPLETED SUCCESSFULLY ")
    logger.info("==================================================")

if __name__ == "__main__":
    run_pipeline()
