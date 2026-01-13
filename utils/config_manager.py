"""Configuration manager for Voice Service Integrated Suite."""
import json
import os
from typing import Any, Dict
from utils.logger import get_logger

logger = get_logger()


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
            else:
                logger.warning(f"Config file not found at {self.config_path}, using defaults")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "api_keys": {},
            "default_settings": {},
            "output_paths": {},
            "cache_settings": {}
        }
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value (e.g., "api_keys.azure_speech_key")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        logger.debug(f"Config updated: {key_path} = {value}")
    
    def get_api_key(self, service: str) -> str:
        """
        Get API key for a specific service.
        
        Args:
            service: Service name (e.g., "azure_speech_key")
            
        Returns:
            API key or empty string
        """
        return self.get(f"api_keys.{service}", "")
    
    def get_output_path(self, output_type: str) -> str:
        """
        Get output path for a specific type.
        
        Args:
            output_type: Output type (e.g., "tts", "stt")
            
        Returns:
            Output path
        """
        path = self.get(f"output_paths.{output_type}", f"output/{output_type}")
        os.makedirs(path, exist_ok=True)
        return path


# Global config manager instance
_config_manager = None


def get_config_manager(config_path: str = "config.json") -> ConfigManager:
    """Get global config manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager
