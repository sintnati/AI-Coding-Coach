@echo off
echo ========================================
echo AI Agent Diagnostic Tool
echo ========================================
echo.

echo [1/6] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK
echo.

echo [2/6] Checking pip...
pip --version
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)
echo OK
echo.

echo [3/6] Checking if dependencies are installed...
python -c "import fastapi" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: fastapi not installed
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo OK - Dependencies appear to be installed
)
echo.

echo [4/6] Testing imports individually...
echo Testing: aiohttp
python -c "import aiohttp; print('  aiohttp OK')"
if %errorlevel% neq 0 (
    echo   ERROR: aiohttp failed to import
)

echo Testing: fastapi
python -c "import fastapi; print('  fastapi OK')"
if %errorlevel% neq 0 (
    echo   ERROR: fastapi failed to import
)

echo Testing: faiss
python -c "import faiss; print('  faiss OK')"
if %errorlevel% neq 0 (
    echo   ERROR: faiss failed to import
)

echo Testing: uvicorn
python -c "import uvicorn; print('  uvicorn OK')"
if %errorlevel% neq 0 (
    echo   ERROR: uvicorn failed to import
)
echo.

echo [5/6] Testing application imports...
python -c "from services.gateway.app import app; print('  App imports OK')"
if %errorlevel% neq 0 (
    echo   ERROR: Application failed to import
    echo   This is the main issue preventing your agent from starting
    echo.
    echo   Common causes:
    echo   - Missing dependencies
    echo   - Syntax errors in code
    echo   - Import cycle
    echo.
    pause
    exit /b 1
)
echo OK
echo.

echo [6/6] Checking .env file...
if not exist .env (
    echo WARNING: .env file not found
    echo Creating from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env and add your GCP credentials before running!
    echo.
) else (
    echo OK - .env exists
)
echo.

echo ========================================
echo Diagnostics Complete!
echo ========================================
echo.
echo All checks passed. Your agent should be able to start.
echo.
echo To start the agent, run: start_agent.bat
echo Or manually run: uvicorn services.gateway.app:app --host 127.0.0.1 --port 8080 --reload
echo.
pause
