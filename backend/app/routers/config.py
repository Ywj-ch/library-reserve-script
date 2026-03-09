from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..services.config_service import ConfigService
from ..models.auth import AuthConfigUpdate
from ..models.reserve import ReserveConfigUpdate

router = APIRouter(prefix="/api/config", tags=["配置管理"])

config_service = ConfigService()


@router.get("")
async def get_config() -> Dict[str, Any]:
    """获取完整配置"""
    try:
        config = config_service.get_full_config()
        auth_config = config_service.get_auth_config()
        config['auth'] = auth_config.model_dump()
        return {
            "success": True,
            "data": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/auth")
async def get_auth_config() -> Dict[str, Any]:
    """获取认证配置"""
    try:
        auth_config = config_service.get_auth_config()
        return {
            "success": True,
            "data": auth_config.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/auth")
async def update_auth_config(auth_update: AuthConfigUpdate) -> Dict[str, Any]:
    """更新认证配置"""
    try:
        updated_config = config_service.update_auth_config(auth_update)
        return {
            "success": True,
            "data": updated_config.model_dump(),
            "message": "认证配置更新成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reserve")
async def get_reserve_config() -> Dict[str, Any]:
    """获取预约配置"""
    try:
        reserve_config = config_service.get_reserve_config()
        return {
            "success": True,
            "data": reserve_config.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/reserve")
async def update_reserve_config(reserve_update: ReserveConfigUpdate) -> Dict[str, Any]:
    """更新预约配置"""
    try:
        updated_config = config_service.update_reserve_config(reserve_update)
        return {
            "success": True,
            "data": updated_config.model_dump(),
            "message": "预约配置更新成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test_config() -> Dict[str, Any]:
    """测试配置有效性"""
    try:
        result = config_service.test_auth_config()
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
