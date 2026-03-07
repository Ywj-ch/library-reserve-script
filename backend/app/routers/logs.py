from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.log_service import LogService

router = APIRouter(prefix="/api/logs", tags=["日志管理"])

log_service = LogService()


@router.get("")
async def get_logs(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    date: Optional[str] = Query(None, description="日期过滤 (YYYY-MM-DD)"),
    status: Optional[str] = Query(None, description="状态过滤 (success/failure)")
):
    """获取日志列表（分页）"""
    try:
        result = log_service.get_logs(
            page=page,
            limit=limit,
            date_filter=date,
            status_filter=status
        )
        return {
            "success": True,
            "data": result.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_log_stats():
    """获取日志统计"""
    try:
        stats = log_service.get_stats()
        return {
            "success": True,
            "data": stats.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
