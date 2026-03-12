@echo off
cls

echo ========================================
echo Backend API Server
echo ========================================
echo.

cd /d "%~dp0"

call ..\.venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
