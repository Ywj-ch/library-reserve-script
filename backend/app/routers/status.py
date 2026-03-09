from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime, timedelta
from ..services.config_service import ConfigService
from ..services.log_service import LogService

router = APIRouter(prefix="/api/status", tags=["状态检查"])

config_service = ConfigService()
log_service = LogService()


@router.get("")
async def get_status() -> Dict[str, Any]:
    """获取系统状态"""
    try:
        auth_config = config_service.get_auth_config()
        reserve_config = config_service.get_reserve_config()
        log_stats = log_service.get_stats()
        
        config_valid = bool(auth_config.cookie and auth_config.code)
        
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        send_time = reserve_config.send_time
        next_run = datetime.combine(tomorrow, datetime.strptime(send_time, "%H:%M:%S").time())
        
        return {
            "success": True,
            "data": {
                "status": "healthy" if config_valid else "warning",
                "config_valid": config_valid,
                "days_remaining": auth_config.days_remaining,
                "next_run": next_run.isoformat(),
                "last_run": log_stats.last_success,
                "last_result": "success" if log_stats.last_success else "unknown",
                "uptime_info": {
                    "total_requests": log_stats.total_requests,
                    "success_rate": log_stats.success_rate
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """健康检查"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
