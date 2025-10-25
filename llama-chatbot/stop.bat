@echo off
echo ========================================
echo Stopping All Services
echo ========================================
echo.

echo [1/3] Stopping Python/Uvicorn...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM py.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1

echo [2/3] Stopping Ollama...
taskkill /F /IM ollama.exe >nul 2>&1
taskkill /F /IM "ollama app.exe" >nul 2>&1
taskkill /F /IM ollama_llama_server.exe >nul 2>&1

echo [3/3] Checking ports...
netstat -ano | findstr :8000
netstat -ano | findstr :11434

echo.
echo ========================================
echo All services stopped
echo ========================================
pause