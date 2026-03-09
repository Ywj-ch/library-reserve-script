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


class SeatAttempt(BaseModel):
    seat_id: str = Field(..., description="座位ID")
    status_code: int = Field(..., description="HTTP状态码")
    response_text: str = Field(..., description="响应内容")
    success: bool = Field(..., description="是否成功")


class LogEntry(BaseModel):
    timestamp: str = Field(..., description="日志时间戳")
    level: LogLevel = Field(..., description="日志级别")
    message: str = Field(..., description="日志消息")
    seat: Optional[str] = Field(None, description="座位ID")
    status: Optional[LogStatus] = Field(None, description="预约状态")


class AggregatedLogEntry(BaseModel):
    session_id: str = Field(..., description="会话ID")
    timestamp: str = Field(..., description="日志时间戳")
    start_time: Optional[str] = Field(None, description="开始时间")
    end_time: Optional[str] = Field(None, description="结束时间")
    status: LogStatus = Field(..., description="预约状态")
    seats: List[SeatAttempt] = Field(default_factory=list, description="座位尝试列表")
    details: List[str] = Field(default_factory=list, description="详细日志")
    success_seat: Optional[str] = Field(None, description="成功的座位ID")
    total_attempts: int = Field(0, description="总尝试次数")
    message: str = Field("", description="摘要消息")


class LogPagination(BaseModel):
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    limit: int = Field(..., description="每页数量")


class LogListResponse(BaseModel):
    logs: List[AggregatedLogEntry] = Field(..., description="日志列表")
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
