from typing import Dict, Any
from datetime import datetime
from ..utils.yaml_handler import YAMLHandler
from ..models.auth import AuthConfig, AuthConfigUpdate, AuthConfigResponse
from ..models.reserve import ReserveConfig, ReserveConfigUpdate


class ConfigService:
    def __init__(self, config_path: str = "config.yaml"):
        self.yaml_handler = YAMLHandler(config_path)
    
    def get_full_config(self) -> Dict[str, Any]:
        return self.yaml_handler.read()
    
    def get_auth_config(self) -> AuthConfigResponse:
        auth_data = self.yaml_handler.get_section('auth')
        
        last_update = datetime.fromisoformat(auth_data.get('last_update', datetime.now().isoformat()))
        expires_days = auth_data.get('expires_days', 10)
        days_passed = (datetime.now() - last_update).days
        days_remaining = max(0, expires_days - days_passed)
        
        return AuthConfigResponse(
            cookie=auth_data.get('cookie', ''),
            code=auth_data.get('code', ''),
            last_update=auth_data.get('last_update', ''),
            days_remaining=days_remaining
        )
    
    def update_auth_config(self, auth_update: AuthConfigUpdate) -> AuthConfig:
        auth_data = {
            'cookie': auth_update.cookie,
            'code': auth_update.code,
            'last_update': datetime.now().isoformat(),
            'expires_days': 10
        }
        self.yaml_handler.update_section('auth', auth_data)
        
        return AuthConfig(**auth_data)
    
    def get_reserve_config(self) -> ReserveConfig:
        reserve_data = self.yaml_handler.get_section('reserve')
        
        if 'datetime_range' not in reserve_data:
            request_data = self.yaml_handler.get_section('request')
            datetime_str = request_data.get('data_template', {}).get('datetime', '660,1350')
            start_minutes, end_minutes = map(int, datetime_str.split(','))
            reserve_data['datetime_range'] = {
                'start': f"{start_minutes // 60:02d}:{start_minutes % 60:02d}",
                'end': f"{end_minutes // 60:02d}:{end_minutes % 60:02d}"
            }
        
        return ReserveConfig(**reserve_data)
    
    def update_reserve_config(self, reserve_update: ReserveConfigUpdate) -> ReserveConfig:
        current_config = self.get_reserve_config()
        
        if reserve_update.send_time is not None:
            current_config.send_time = reserve_update.send_time
        
        if reserve_update.seats is not None:
            current_config.seats = reserve_update.seats
        
        if reserve_update.datetime_range is not None:
            current_config.datetime_range = reserve_update.datetime_range
            
            start_parts = reserve_update.datetime_range.start.split(':')
            end_parts = reserve_update.datetime_range.end.split(':')
            start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
            end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
            
            config = self.yaml_handler.read()
            if 'request' not in config:
                config['request'] = {}
            if 'data_template' not in config['request']:
                config['request']['data_template'] = {}
            config['request']['data_template']['datetime'] = f"{start_minutes},{end_minutes}"
            self.yaml_handler.write(config)
        
        self.yaml_handler.update_section('reserve', current_config.model_dump())
        
        return current_config
    
    def test_auth_config(self) -> Dict[str, Any]:
        auth_config = self.get_auth_config()
        
        is_valid = bool(auth_config.cookie and auth_config.code)
        
        return {
            'valid': is_valid,
            'message': '配置有效' if is_valid else 'Cookie 或 Code 为空',
            'days_remaining': auth_config.days_remaining
        }
