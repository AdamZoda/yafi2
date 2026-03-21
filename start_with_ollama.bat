@echo off
REM ============================================
REM YAFI with Ollama - Quick Start Script
REM ============================================

echo.
echo ==================================================
echo.        YAFI Ollama Integration Launcher
echo ==================================================
echo.

REM Check if Ollama is running
echo [1/4] Checking Ollama...
timeout /t 1 /nobreak > nul
curl http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Ollama is not running!
    echo.
    echo ^> Start Ollama by opening a new terminal and running:
    echo.
    echo    ollama serve
    echo.
    pause
    exit /b 1
)
echo ✓ Ollama is accessible

REM Install dependencies
echo.
echo [2/4] Checking Dependencies...
timeout /t 1 /nobreak > nul
python -m pip install flask flask-cors requests python-dotenv >nul 2>&1
echo ✓ Dependencies ready

REM Check Python version
echo.
echo [3/4] Verifying Python...
timeout /t 1 /nobreak > nul
python --version
echo ✓ Python is ready

REM Start the backend server
echo.
echo [4/4] Starting Backend Server...
echo.
cd backend
python server.py

pause
