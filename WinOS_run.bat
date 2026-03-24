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

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo Python found: %pyver%

:: Ensure pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available.
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
    echo [WARNING] ffmpeg not found. Attempting to install via winget...
    winget --version >nul 2>&1
    if not errorlevel 1 (
        winget install -e --id Gyan.FFmpeg --silent
        if errorlevel 1 (
            echo [ERROR] winget install failed. Install ffmpeg manually from https://ffmpeg.org
        ) else (
            echo ffmpeg installed. You may need to restart your terminal.
        )
    ) else (
        echo [ERROR] winget not found. Install ffmpeg manually from https://ffmpeg.org
        pause
        exit /b 1
    )
) else (
    echo ffmpeg found.
)

:: Install Flask + mutagen
echo Installing Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: FIX #1: Start server and capture its PID properly
echo Starting yt-dlp Web UI...
start "" /b python app.py
set APP_PID=

:: Wait for server to be ready
timeout /t 3 /nobreak >nul

:: Get PID of the python process running app.py
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo list ^| findstr "PID:"') do (
    for /f "tokens=*" %%b in ('wmic process where "ProcessId=%%a" get CommandLine /value 2^>nul ^| findstr "app.py"') do (
        set APP_PID=%%a
    )
)

:: Open browser
start http://localhost:5000

echo =============================================
echo Web UI running at http://localhost:5000
echo Press any key to STOP the server only.
echo =============================================
pause >nul

:: FIX #1: Kill only the specific python process running app.py
if defined APP_PID (
    echo Stopping server (PID: %APP_PID%)...
    taskkill /f /pid %APP_PID% >nul 2>&1
) else (
    echo Could not find server PID. Searching by window...
    wmic process where "name='python.exe' and CommandLine like '%%app.py%%'" delete >nul 2>&1
)

echo Server stopped.
