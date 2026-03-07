import yaml
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import threading


class YAMLHandler:
    _lock = threading.Lock()
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        if not self.config_path.is_absolute():
            self.config_path = Path(__file__).parent.parent.parent.parent / config_path
    
    def read(self) -> Dict[str, Any]:
        with self._lock:
            if not self.config_path.exists():
                raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
    
    def write(self, config: Dict[str, Any]) -> None:
        with self._lock:
            if 'metadata' not in config:
                config['metadata'] = {}
            config['metadata']['updated_at'] = datetime.now().isoformat()
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    def update_section(self, section: str, data: Dict[str, Any]) -> None:
        config = self.read()
        if section not in config:
            config[section] = {}
        config[section].update(data)
        self.write(config)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        config = self.read()
        return config.get(section, {})
    
    def exists(self) -> bool:
        return self.config_path.exists()
    
    def create_default(self) -> None:
        default_config = {
            'auth': {
                'cookie': '',
                'code': '',
                'last_update': datetime.now().isoformat(),
                'expires_days': 10
            },
            'reserve': {
                'send_time': '07:00:02',
                'seats': [],
                'retry': {
                    'max_attempts': 3,
                    'delay_seconds': 1
                }
            },
            'request': {
                'url': 'https://libwx.hunnu.edu.cn/apim/seat/SeatDateHandler.ashx',
                'data_template': {
                    'data_type': 'seatDate',
                    'seatdate': 'today',
                    'datetime': '660,1350'
                }
            },
            'metadata': {
                'version': '1.0.0',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        }
        self.write(default_config)
