@echo off
echo ==========================================
echo   AI DevOps Agent - Quick Demo Launcher
echo ==========================================
echo.
echo Starting FastAPI Backend on port 7860...
start "Backend Server" cmd /k "cd /d c:\AI_DeVops\github_agent_backend && ..\.venv\Scripts\python.exe -m uvicorn server.app:app --host 0.0.0.0 --port 7860"
echo Waiting 4 seconds for backend to boot up...
timeout /t 4 /nobreak >nul
echo.
echo Triggering mock GitHub webhook failure (syntax error)...
..\.venv\Scripts\python.exe trigger.py syntax
echo.
echo Please check the "Backend Server" window to see the Agents in action!
echo.
echo To also start the Streamlit Dashboard, run:
echo   streamlit run dashboard.py
pause
