from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import config, logs, status

app = FastAPI(
    title="图书馆座位预约助手 API",
    description="基于 FastAPI 的图书馆座位预约管理系统后端 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config.router)
app.include_router(logs.router)
app.include_router(status.router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "图书馆座位预约助手 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api")
async def api_root():
    """API 根路径"""
    return {
        "message": "欢迎使用图书馆座位预约助手 API",
        "endpoints": {
            "config": "/api/config",
            "logs": "/api/logs",
            "status": "/api/status"
        }
    }
