import os
import logging
from typing import Optional, Dict, Any
import json
import hashlib
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def load_config(file_path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {file_path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in config file: {file_path}")
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
    return None

def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def validate_token(token: str, secret: str) -> bool:
    try:
        payload, signature = token.rsplit('.', 1)
        expected_signature = generate_hash(f"{payload}{secret}")
        return signature == expected_signature
    except ValueError:
        return False

def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)

def format_timestamp(timestamp: datetime) -> str:
    return timestamp.isoformat()

def get_expiration_time(minutes: int = 30) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)

def ensure_dir_exists(dir_path: str) -> bool:
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except OSError as e:
        logger.error(f"Error creating directory {dir_path}: {e}")
        return False