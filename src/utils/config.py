import yaml
import os

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.data = self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("❌ Config file not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Return default configuration"""
        return {
            'app': {
                'name': 'Snapp Buyer',
                'version': '1.0.0'
            },
            'snapp': {
                'login_url': 'https://app.snapp.taxi/login',
                'snapp_pay_url': 'https://snapppay.ir/timetable/',
                'phone_number': '09014282751'
            },
            'monitor': {
                'refresh_interval': 2,
                'max_retries': 10,
                'timeout': 30
            },
            'products': {
                'priority_list': [
                    "Samsung S25 Ultra Mobile",
                    "Asus Vivobook X1504VA Laptop", 
                    "Sony PlayStation 5 Slim",
                    "Anker SoundCore R50i Headphones",
                    "Samsung Galaxy A16 4G Mobile"
                ]
            },
            'browser': {
                'headless': False,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
    
    def get(self, key_path, default=None):
        """Get configuration value by dot notation path"""
        keys = key_path.split('.')
        value = self.data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.data, file, allow_unicode=True)