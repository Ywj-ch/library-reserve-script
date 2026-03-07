@echo off
chcp 65001 >nul
cls

echo ========================================
echo Library Reserve - Quick Start
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Starting Backend...
start "Backend API" cmd /k "cd .. && backend\venv\Scripts\python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend...
cd ..\frontend
start "Frontend Dev" cmd /k "npm run dev"

timeout /t 5 /nobreak >nul

echo [3/3] Opening Browser...
start http://localhost:5173

echo.
echo ========================================
echo All services started successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Two command windows opened:
echo   - Backend API (Port 8000)
echo   - Frontend Dev (Port 5173)
echo.
echo Keep windows open to keep services running
echo ========================================
echo.

pause
