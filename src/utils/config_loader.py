import os
import yaml
from typing import Any, Dict

def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """Loads a YAML configuration file safely."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found at: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config
