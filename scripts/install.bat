@echo off
chcp 65001
echo ====================================
echo 图书馆座位预约助手 - 依赖安装
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] 检查 Python...
python --version
if errorlevel 1 (
    echo 错误: Python 未安装或未添加到 PATH
    pause
    exit /b 1
)

echo.
echo [2/3] 创建虚拟环境...
if not exist "backend\venv" (
    python -m venv backend\venv
    echo 虚拟环境创建完成
) else (
    echo 虚拟环境已存在
)

echo.
echo [3/3] 安装后端依赖...
call backend\venv\Scripts\activate
pip install --upgrade pip
pip install -r backend\requirements.txt

echo.
echo ====================================
echo 安装完成！
echo ====================================
echo 后端依赖已安装到 backend\venv
echo 请运行 start_backend.bat 启动后端服务
echo ====================================
echo.

pause
