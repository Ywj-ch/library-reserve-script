import sys
import asyncio
from pathlib import Path
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

router = APIRouter(prefix="/api/reserve", tags=["预约执行"])

executor = ThreadPoolExecutor(max_workers=1)


def run_reserve_sync() -> Dict[str, Any]:
    project_root = Path(__file__).parent.parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    from reserve_seat import run_reservation
    return run_reservation(immediate=True)


class RunResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str


@router.post("/run", response_model=RunResponse)
async def run_reserve() -> RunResponse:
    """手动执行预约任务"""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, run_reserve_sync)
        
        if result["status"] == "success":
            return RunResponse(
                success=True,
                data=result,
                message=f"预约成功！座位: {result.get('success_seat', '未知')}"
            )
        else:
            return RunResponse(
                success=False,
                data=result,
                message=f"预约失败，共尝试 {result['total_attempts']} 个座位"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败: {str(e)}")
