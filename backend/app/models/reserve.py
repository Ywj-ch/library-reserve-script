from pydantic import BaseModel, Field
from typing import List, Optional


class Seat(BaseModel):
    id: str = Field(..., description="座位ID")
    name: str = Field(..., description="座位名称")
    enabled: bool = Field(default=True, description="是否启用")


class RetryConfig(BaseModel):
    delay_seconds: int = Field(default=1, description="重试延迟秒数")


class DatetimeRange(BaseModel):
    start: str = Field(default="11:00", description="开始时间（HH:MM）")
    end: str = Field(default="22:30", description="结束时间（HH:MM）")


class ReserveConfig(BaseModel):
    send_time: str = Field(default="07:00:02", description="发送时间（HH:MM:SS）")
    seats: List[Seat] = Field(default_factory=list, description="座位列表")
    retry: RetryConfig = Field(default_factory=RetryConfig, description="重试配置")
    datetime_range: Optional[DatetimeRange] = Field(default_factory=DatetimeRange, description="预约时间段")


class ReserveConfigUpdate(BaseModel):
    send_time: Optional[str] = Field(None, description="发送时间（HH:MM:SS）")
    seats: Optional[List[Seat]] = Field(None, description="座位列表")
    datetime_range: Optional[DatetimeRange] = Field(None, description="预约时间段")

    class Config:
        json_schema_extra = {
            "example": {
                "send_time": "07:00:05",
                "seats": [
                    {"id": "Z41N001", "name": "001", "enabled": True},
                    {"id": "Z405002", "name": "002", "enabled": True}
                ],
                "datetime_range": {"start": "11:00", "end": "22:30"}
            }
        }
