@echo off
setlocal

set REPO_ROOT=%~dp0..
pushd "%REPO_ROOT%"

for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8010 " ^| findstr LISTENING') do (
  taskkill /PID %%p /F >nul 2>&1
)

start "DEIA RAQCOON API" cmd /k "python deia_raqcoon\runtime\run_server.py"
start "" "docs\mockups\hive-chat-mockup-operator.html"

popd
