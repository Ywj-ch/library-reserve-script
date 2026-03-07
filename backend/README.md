# Backend - FastAPI Server

FastAPI 后端服务，提供配置管理、日志查询等 API 接口。

## 快速启动

### 方式 1: 双击启动（Windows）
```
双击: run.bat
```

### 方式 2: 命令行启动
```bash
# 激活虚拟环境
venv\Scripts\activate

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 访问地址
- API 服务: http://localhost:8000
- API 文档 (Swagger): http://localhost:8000/docs
- API 文档 (ReDoc): http://localhost:8000/redoc

## 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## API 接口

### 配置管理
- `GET /api/config` - 获取完整配置
- `GET /api/config/auth` - 获取认证配置
- `PUT /api/config/auth` - 更新认证配置
- `GET /api/config/reserve` - 获取预约配置
- `PUT /api/config/reserve` - 更新预约配置
- `POST /api/config/test` - 测试配置有效性

### 日志管理
- `GET /api/logs` - 获取日志列表（支持分页）
- `GET /api/logs/stats` - 获取日志统计

### 状态检查
- `GET /api/status` - 获取系统状态
- `GET /api/status/health` - 健康检查

## 测试 API

### 使用浏览器
访问 http://localhost:8000/docs 使用 Swagger UI 进行交互式测试。

### 使用 curl

```bash
# 获取配置
curl http://localhost:8000/api/config

# 获取状态
curl http://localhost:8000/api/status

# 更新认证配置
curl -X PUT http://localhost:8000/api/config/auth \
  -H "Content-Type: application/json" \
  -d '{"cookie": "your_cookie", "code": "your_code"}'

# 更新预约配置
curl -X PUT http://localhost:8000/api/config/reserve \
  -H "Content-Type: application/json" \
  -d '{
    "send_time": "07:00:05",
    "seats": [
      {"id": "Z41N001", "name": "001", "enabled": true}
    ]
  }'
```

## 项目结构

```
backend/
├── app/
│   ├── main.py          # FastAPI 应用入口
│   ├── config.py        # 全局配置
│   ├── models/          # Pydantic 数据模型
│   ├── services/        # 业务逻辑层
│   ├── routers/         # API 路由
│   └── utils/           # 工具函数
├── venv/                # Python 虚拟环境
├── requirements.txt     # 依赖列表
└── run.bat              # Windows 启动脚本
```

## 常见问题

### Q: 端口 8000 被占用怎么办？
A: 修改启动命令中的端口号：
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Q: 如何查看日志？
A: 日志文件位于项目根目录 `logs/reserve_seat.log`

### Q: 配置文件在哪里？
A: 配置文件位于项目根目录 `config.yaml`

### Q: 如何停止服务器？
A: 在运行服务器的终端按 `Ctrl+C`
