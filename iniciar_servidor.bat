@echo off
title ArchivaIA - Servidor Backend API
echo ============================================================
echo   Iniciando ArchivaIA API Backend (FastAPI + Gemini + Supabase)
echo   INACAP Sede Maipu
echo ============================================================
echo.
py -3.12 run_server.py 2>nul || py run_server.py 2>nul || python run_server.py
pause
