import json
import os

class ConfigManager:
    """配置管理类，用于加载和保存配置文件"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            "main_window": {
                "width": 800,
                "height": 600,
                "x": 100,
                "y": 100
            },
            "secondary_window": {
                "width": 800,
                "height": 600,
                "x": 1000,
                "y": 100
            },
            "scroll_speed": 1000,
            "font_size": 36,
            "background_color": "#000000",
            "text_color": "#ffffff",
            "paragraph_duration": 10,
            "paragraph_time_control_mode": "global",
            "secondary_screen_topmost": False,
            "main_window_topmost": False,
            "last_opened_file": None
        }
        self.config = self.default_config.copy()
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                self.config.update(loaded_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                self.config = self.default_config.copy()
        else:
            self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
    
    def update_window_size(self, window_type, width, height):
        """更新窗口大小配置"""
        self.set(f"{window_type}.width", width)
        self.set(f"{window_type}.height", height)
    
    def update_window_position(self, window_type, x, y):
        """更新窗口位置配置"""
        self.set(f"{window_type}.x", x)
        self.set(f"{window_type}.y", y)
