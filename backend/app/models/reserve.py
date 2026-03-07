from pydantic import BaseModel, Field
from typing import List, Optional


class Seat(BaseModel):
    id: str = Field(..., description="座位ID")
    name: str = Field(..., description="座位名称")
    enabled: bool = Field(default=True, description="是否启用")


class RetryConfig(BaseModel):
    max_attempts: int = Field(default=3, description="最大尝试次数")
    delay_seconds: int = Field(default=1, description="重试延迟秒数")


class ReserveConfig(BaseModel):
    send_time: str = Field(default="07:00:02", description="发送时间（HH:MM:SS）")
    seats: List[Seat] = Field(default_factory=list, description="座位列表")
    retry: RetryConfig = Field(default_factory=RetryConfig, description="重试配置")


class ReserveConfigUpdate(BaseModel):
    send_time: Optional[str] = Field(None, description="发送时间（HH:MM:SS）")
    seats: Optional[List[Seat]] = Field(None, description="座位列表")

    class Config:
        json_schema_extra = {
            "example": {
                "send_time": "07:00:05",
                "seats": [
                    {"id": "Z41N001", "name": "001", "enabled": True},
                    {"id": "Z405002", "name": "002", "enabled": True}
                ]
            }
        }
