@echo off
cls

echo ========================================
echo Starting Frontend Dev Server
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Vite development server...
npm run dev
