#!/usr/bin/env python3
"""
Configuration Manager for Terminal Chat Bluetooth
Handles loading and managing application settings
"""

import json
import os
from pathlib import Path

class Config:
    """Configuration manager"""
    
    DEFAULT_CONFIG = {
        "bluetooth": {
            "port": 1,
            "scan_duration": 8,
            "auto_accept_files": True,
            "max_file_size_mb": 50
        },
        "tcp_fallback": {
            "host": "localhost",
            "port": 8888
        },
        "ui": {
            "use_colors": True,
            "show_timestamps": True,
            "max_history_lines": 100
        },
        "file_transfer": {
            "chunk_size": 1024,
            "downloads_dir": "~/Downloads/BluetoothChat",
            "show_progress": True
        },
        "security": {
            "require_pairing": False,
            "log_connections": True
        }
    }
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
                print("Using default configuration")
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
    
    def get(self, key_path, default=None):
        """Get configuration value by dot-separated path"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """Set configuration value by dot-separated path"""
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def expand_path(self, path):
        """Expand user path (~) to absolute path"""
        if isinstance(path, str) and path.startswith('~'):
            return str(Path(path).expanduser())
        return path
    
    def get_downloads_dir(self):
        """Get downloads directory as Path object"""
        downloads_dir = self.get('file_transfer.downloads_dir')
        expanded = self.expand_path(downloads_dir)
        path = Path(expanded)
        path.mkdir(parents=True, exist_ok=True)
        return path

# Global config instance
config = Config()
