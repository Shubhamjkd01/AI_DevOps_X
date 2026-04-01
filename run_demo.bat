@echo off
echo Starting GitHub Webhook Backend on port 8080...
start "Backend Server" cmd /k "python main.py"
echo Waiting 3 seconds for backend to boot up...
timeout /t 3 /nobreak >nul
echo Triggering mock GitHub webhook failure...
python trigger.py
echo.
echo Please look at the new "Backend Server" window that popped up to see the Agents in action!
pause
