@echo off
cd /d "%~dp0backend"
echo Starting BharatAI Backend on port 8000...
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
