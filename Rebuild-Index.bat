@echo off
title Deep Roots — Rebuild index.html
cd /d "%~dp0"
node "code-sections\rebuild-index.js"
echo.
pause
