@echo off
cd /d "%~dp0"
echo Installing dependencies...
pip install fastapi uvicorn aiohttp
echo.
echo Starting Llama Chatbot...
py app.py
pause

