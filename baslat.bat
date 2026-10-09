@echo off
title YouTube Medya Indirici - Streamlit
echo ====================================================
echo   YouTube Video ve MP3 Indirici Baslatiliyor...
echo ====================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [.venv] Sanal ortam bulunamadi!
    pause
    exit /b
)

echo Tarayici aciliyor: http://localhost:8501
start http://localhost:8501
.\.venv\Scripts\streamlit.exe run app.py
pause
