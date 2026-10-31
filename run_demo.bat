@echo off
echo ==========================================
echo   AI DevOps Agent - Full Demo Launcher
echo   Powered by Google Gemma 4
echo ==========================================
echo.
echo 1. Starting FastAPI Backend on port 7860...
start "AI DevOps Backend" cmd /k "python -m uvicorn server.app:app --host 0.0.0.0 --port 7860"

echo 2. Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak >nul

echo 3. Starting Streamlit Command Center on port 8501...
start "AI DevOps Dashboard" cmd /k "streamlit run dashboard.py"

echo 4. Triggering test GitHub Actions failure triage...
python scripts\trigger.py syntax

echo.
echo ==========================================
echo   Demo running! 
echo   - Backend:   http://localhost:7860
echo   - Dashboard: http://localhost:8501
echo ==========================================
pause
