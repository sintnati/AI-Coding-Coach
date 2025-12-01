@echo off
echo Starting AI Coding Coach Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
python -m uvicorn services.gateway.app:app --host 127.0.0.1 --port 8080 --reload
