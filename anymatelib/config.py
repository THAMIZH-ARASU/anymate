"""Configuration management for Anymate."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Manages configuration for Anymate."""
    
    def __init__(self):
        self._config = {}
        self._load_defaults()
        self._load_custom_config()
    
    def _load_defaults(self):
        """Load default configuration."""
        default_config_path = Path(__file__).parent / "default_config.yml"
        if default_config_path.exists():
            with open(default_config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        else:
            self._config = {}
    
    def _load_custom_config(self):
        """Load custom configuration if it exists."""
        custom_config_path = Path("custom_config.yml")
        if custom_config_path.exists():
            with open(custom_config_path, 'r') as f:
                custom = yaml.safe_load(f)
                if custom:
                    self._config.update(custom)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set a configuration value."""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update configuration with dictionary."""
        for key, value in updates.items():
            self.set(key, value)
    
    def apply_quality_preset(self, quality: str):
        """Apply a quality preset."""
        presets = self.get('quality_presets', {})
        if quality in presets:
            preset = presets[quality]
            self.update(preset)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()


# Global configuration instance
_global_config = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def reset_config():
    """Reset the global configuration instance."""
    global _global_config
    _global_config = None
