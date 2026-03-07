from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class LogStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"


class LogEntry(BaseModel):
    timestamp: str = Field(..., description="日志时间戳")
    level: LogLevel = Field(..., description="日志级别")
    message: str = Field(..., description="日志消息")
    seat: Optional[str] = Field(None, description="座位ID")
    status: Optional[LogStatus] = Field(None, description="预约状态")


class LogPagination(BaseModel):
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    limit: int = Field(..., description="每页数量")


class LogListResponse(BaseModel):
    logs: List[LogEntry] = Field(..., description="日志列表")
    pagination: LogPagination = Field(..., description="分页信息")


class LogStats(BaseModel):
    total_requests: int = Field(..., description="总请求数")
    success_count: int = Field(..., description="成功次数")
    failure_count: int = Field(..., description="失败次数")
    success_rate: float = Field(..., description="成功率")
    last_success: Optional[str] = Field(None, description="最后成功时间")

    class Config:
        json_schema_extra = {
            "example": {
                "total_requests": 30,
                "success_count": 28,
                "failure_count": 2,
                "success_rate": 93.33,
                "last_success": "2025-03-07T07:00:02"
            }
        }
