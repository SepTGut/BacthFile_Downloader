#!/bin/bash
set -e

echo "============================================="
echo "yt-dlp Web UI - Setup and Run (macOS)"
echo "============================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python found: $PY_VERSION"

# Ensure pip
if ! python3 -m pip --version &> /dev/null; then
    echo "[ERROR] pip is not available. Please ensure pip is installed."
    exit 1
fi

# Install/upgrade yt-dlp
echo "Installing/upgrading yt-dlp..."
python3 -m pip install -U yt-dlp

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "[WARNING] ffmpeg not found. Attempting to install via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "[ERROR] Homebrew not found. Please install Homebrew first: https://brew.sh/"
        exit 1
    fi
    brew install ffmpeg
else
    echo "ffmpeg found."
fi

# Install Flask
echo "Installing Flask..."
python3 -m pip install -r requirements.txt

# Run app in background
echo "Starting yt-dlp Web UI..."
python3 app.py &
APP_PID=$!

# Wait for server to start
sleep 3

# Open browser
open http://localhost:5000

echo "============================================="
echo "Web UI should be opening in your browser."
echo "Press Ctrl+C to stop the server."
wait $APP_PID