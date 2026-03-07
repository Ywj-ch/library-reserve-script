# 图书馆座位预约助手

一个现代化的图书馆座位预约自动化管理系统，具有美观的 Web 界面和强大的后端 API。

## 功能特性

- **热启动机制**: 提前启动程序，精准时间点发送预约请求
- **现代化界面**: Vue 3 + TypeScript + Tailwind CSS
- **可视化配置**: Web 界面管理所有配置，无需修改代码
- **日志分析**: 完整的日志记录和统计分析功能
- **座位管理**: 可视化管理座位列表，支持优先级调整

## 技术栈

**后端**: FastAPI + Pydantic + PyYAML + uvicorn

**前端**: Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia

## 快速启动

### 方式 1: 分别启动（推荐）

**启动后端**：
```bash
cd backend
run.bat
# 或双击 run.bat
```

**启动前端**（新终端）：
```bash
cd frontend
run.bat
# 或双击 run.bat
```

**访问地址**：
- 前端界面: http://localhost:5173
- API 文档: http://localhost:8000/docs

### 方式 2: 一键启动

```bash
cd scripts
start_all.bat
```

## 安装

### 前置要求
- Python 3.8+
- Node.js 16+

### 快速安装

```bash
# 安装所有依赖
cd scripts
install.bat
```

或手动安装：

**后端**：
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**前端**：
```bash
cd frontend
npm install
```

## 配置说明

### 首次使用

1. 打开浏览器访问 http://localhost:5173
2. 在"认证配置"部分输入从微信抓包获取的 Cookie 和 Code
3. 在"座位列表"中添加您想要预约的座位
4. 调整"发送时间"（建议 07:00:02）
5. 保存配置

### 配置文件结构

配置文件位于 `config.yaml`：

```yaml
auth:
  cookie: "your_cookie_here"
  code: "your_code_here"
  last_update: "2026-03-07T10:30:25"
  expires_days: 10

reserve:
  send_time: "07:00:02"
  seats:
    - id: "Z41N001"
      name: "001"
      enabled: true
  retry:
    max_attempts: 3
    delay_seconds: 1
```

### 更新配置

**方式 1: 使用 Web 界面（推荐）**
访问 http://localhost:5173，在界面中更新配置

**方式 2: 手动编辑**
直接编辑 `config.yaml` 文件

## 定时任务设置

使用 Windows 任务计划程序设置定时任务：

1. 打开"任务计划程序"（Win + R → 输入 `taskschd.msc`）
2. 创建基本任务
3. 触发器：每天 06:50
4. 操作：启动程序
   - 程序：`python.exe` 的完整路径
   - 参数：`reserve_seat.py`
   - 起始位置：项目根目录

## 项目结构

```
library-reserve-script/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── main.py      # 应用入口
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务逻辑
│   │   ├── routers/     # API 路由
│   │   └── utils/       # 工具函数
│   ├── requirements.txt
│   └── run.bat
│
├── frontend/             # Vue 3 前端
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面
│   │   ├── api/         # API 调用
│   │   ├── stores/      # 状态管理
│   │   └── types/       # TypeScript 类型
│   ├── package.json
│   └── run.bat
│
├── scripts/              # 辅助脚本
│   ├── install.bat      # 一键安装
│   ├── start_all.bat    # 一键启动
│   ├── test_reserve.py  # 测试配置
│   └── clean_logs.py    # 清理日志
│
├── config.yaml           # 配置文件
├── reserve_seat.py       # 主预约脚本
└── logs/                 # 日志目录
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
- `GET /api/logs` - 获取日志列表（分页）
- `GET /api/logs/stats` - 获取日志统计

### 状态检查
- `GET /api/status` - 获取系统状态
- `GET /api/status/health` - 健康检查

详细 API 文档：http://localhost:8000/docs

## 测试

```bash
# 测试配置是否正确
python scripts\test_reserve.py

# 运行预约脚本
python reserve_seat.py
```

## 日志管理

```bash
# 查看日志
type logs\reserve_seat.log

# 清理旧日志（默认保留 30 天）
python scripts\clean_logs.py
```

## 常见问题

### Q1: 如何测试预约脚本？
A: 运行 `python scripts\test_reserve.py`

### Q2: 如何立即运行预约？
A: 修改 config.yaml 中的 send_time 为当前时间后2分钟，然后运行 `python reserve_seat.py`

### Q3: 如何查看日志？
A: 
- Web 界面: http://localhost:5173 (日志页面)
- 文件: `logs/reserve_seat.log`

### Q4: Cookie 多久过期？
A: 大约 10 天，Web 界面会显示剩余天数

### Q5: 如何更新 Cookie？
A: 
1. 使用 Fiddler 重新抓包
2. 在 Web 界面更新
3. 或直接编辑 config.yaml

### Q6: 端口被占用怎么办？
A: 
- 后端：修改 `backend/run.bat` 中的端口号
- 前端：Vite 会自动使用下一个可用端口

### Q7: 日志文件太大怎么办？
A: 运行 `python scripts\clean_logs.py` 清理旧日志

## 最佳实践

1. **定期更新配置**: 每 7-10 天更新一次 Cookie 和 Code
2. **监控日志**: 定期查看 Web 界面的日志页面
3. **测试配置**: 更新配置后运行测试脚本验证
4. **备份配置**: 定期备份 config.yaml
5. **清理日志**: 每月运行一次日志清理脚本

## 注意事项

1. **安全警告**: 绝不将包含 Cookie 和 Code 的 `config.yaml` 提交到版本控制
2. **配置过期**: Cookie 和 Code 大约 10 天过期，需要定期更新
3. **合法使用**: 仅用于学习交流，请勿用于非法用途
4. **频率控制**: 不要短时间内多次访问服务器，避免被封禁

## 许可证

MIT License
