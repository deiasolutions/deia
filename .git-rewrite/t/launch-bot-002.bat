@echo off
REM Launch CLAUDE-CODE-002 with clean environment (no ANTHROPIC_API_KEY conflict)

echo [LAUNCH] Clearing ANTHROPIC_API_KEY for this session...
set ANTHROPIC_API_KEY=

echo [LAUNCH] Changing to project directory...
cd /d C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions

echo [LAUNCH] Starting Claude Code for bot 002...
echo [LAUNCH] Read launch instructions: .deia\handoffs\CLAUDE-CODE-002-LAUNCH-2025-10-24.md
echo.

claude
