@echo off
echo ========================================
echo Restarting Llama Chatbot Services
echo ========================================
echo.

REM Kill all Python processes (this will stop app.py)
echo [1/4] Stopping Python services...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM py.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Kill any uvicorn processes
echo [2/4] Stopping Uvicorn...
taskkill /F /IM uvicorn.exe >nul 2>&1
timeout /t 1 /nobreak >nul

REM Check if Ollama is running, if not start it
echo [3/4] Checking Ollama...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Ollama is already running
) else (
    echo Starting Ollama...
    start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama app.exe"
    timeout /t 3 /nobreak >nul
)

REM Start the app
echo [4/4] Starting Llama Chatbot...
echo.
echo ========================================
echo Services starting...
echo Chat will be available at: http://localhost:8000
echo Press Ctrl+C to stop
echo ========================================
echo.

cd /d "%~dp0"
python app.py

pause