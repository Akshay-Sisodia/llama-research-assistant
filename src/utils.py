import os
from typing import Any, Optional

def get_env_variable(key: str, default: Optional[Any] = None) -> str:
    """Safely get environment variable with optional default."""
    value = os.getenv(key)
    if value is None:
        if default is not None:
            return default
        raise ValueError(f"Environment variable {key} not set and no default provided")
    return value