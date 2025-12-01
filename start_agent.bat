@echo off
echo Starting AI Agent Gateway...
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your GCP credentials!
    echo.
    pause
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server in background and open Chrome
echo.
echo Starting server on http://localhost:8080
echo Opening Chrome browser...
echo.
echo Press Ctrl+C to stop the server
echo.

REM Open Chrome after a short delay
start "" timeout /t 3 /nobreak >nul && start chrome http://localhost:8080

REM Start the server (this will block)
uvicorn services.gateway.app:app --host 127.0.0.1 --port 8080 --reload

