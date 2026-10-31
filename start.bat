@echo off
echo ==========================================
echo   Starting AI DevOps Agent Services
echo ==========================================
echo.
echo 1. Starting FastAPI Webhook Backend on port 7860...
start "AI DevOps Backend" cmd /k "python -m uvicorn server.app:app --host 0.0.0.0 --port 7860"

echo 2. Starting Streamlit Dashboard on port 8501...
start "AI DevOps Dashboard" cmd /k "streamlit run dashboard.py"

echo Services running! Check the opened terminal windows.
