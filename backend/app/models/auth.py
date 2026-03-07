from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AuthConfig(BaseModel):
    cookie: str = Field(..., description="用户认证 Cookie")
    code: str = Field(..., description="预约验证码")
    last_update: str = Field(default_factory=lambda: datetime.now().isoformat(), description="最后更新时间")
    expires_days: int = Field(default=10, description="过期天数")


class AuthConfigUpdate(BaseModel):
    cookie: str = Field(..., description="用户认证 Cookie")
    code: str = Field(..., description="预约验证码")


class AuthConfigResponse(BaseModel):
    cookie: str
    code: str
    last_update: str
    days_remaining: int = Field(..., description="剩余天数")

    class Config:
        json_schema_extra = {
            "example": {
                "cookie": "ASP.NET_SessionId=xxx; cookie_unit_name=xxx",
                "code": "637F5C6974337A230B5D40E2...",
                "last_update": "2025-03-07T10:30:25",
                "days_remaining": 7
            }
        }
