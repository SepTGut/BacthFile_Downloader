@echo off
setlocal enabledelayedexpansion

echo =============================================
echo yt-dlp Web UI - Setup and Run
echo =============================================

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8 or later from https://python.org
    pause
    exit /b 1
)

:: Check Python version (simple)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo Python found: %pyver%

:: Ensure pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available. Please ensure pip is installed.
    pause
    exit /b 1
)

:: Install/upgrade yt-dlp
echo Installing/upgrading yt-dlp...
python -m pip install -U yt-dlp
if errorlevel 1 (
    echo [ERROR] Failed to install yt-dlp.
    pause
    exit /b 1
)

:: Check ffmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] ffmpeg not found. Attempting to install...
    :: Try winget (Windows Package Manager)
    winget --version >nul 2>&1
    if not errorlevel 1 (
        echo Installing ffmpeg via winget...
        winget install -e --id Gyan.FFmpeg --silent
        if errorlevel 1 (
            echo [ERROR] winget installation failed. Please install ffmpeg manually.
        ) else (
            echo ffmpeg installed via winget.
        )
    ) else (
        echo [ERROR] ffmpeg not found and no winget. Please install ffmpeg manually from https://ffmpeg.org/download.html
        pause
        exit /b 1
    )
) else (
    echo ffmpeg found.
)

:: Install Flask
echo Installing Flask...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Flask.
    pause
    exit /b 1
)

:: Start server in background
start /b python app.py

:: Wait for server to start
timeout /t 3 /nobreak >nul

:: Open browser
start http://localhost:5000

echo =============================================
echo Web UI should be opening in your browser.
echo Press any key to stop the server and close this window.
pause >nul
taskkill /f /im python.exe /fi "windowtitle eq app.py" >nul 2>&1