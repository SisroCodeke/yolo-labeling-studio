"""
Configuration management utilities
"""

import os
import json
import copy
from typing import Dict, Any
from .default_config import DEFAULT_CONFIG


def deep_merge(base: Dict, override: Dict) -> Dict:
    """Optimized deep merge with type checking"""
    if not isinstance(override, dict):
        return override
    
    result = copy.deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config(path: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file with fallback to defaults
    
    Args:
        path: Path to configuration file
        
    Returns:
        Merged configuration dictionary
    """
    cfg = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception as e:
            print(f"[WARN] Failed to parse {path}: {e}")
    
    return deep_merge(DEFAULT_CONFIG, cfg)
