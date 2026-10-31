@echo off
echo ========================================================
echo   AIDEVOPS - Windows 1-Click Startup Launcher
echo ========================================================
echo.

if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env
        echo [*] Created .env from .env.example.
        echo [*] Please edit .env with your GEMINI_API_KEY and GITHUB_TOKEN!
    )
)

python run_local.py
pause
