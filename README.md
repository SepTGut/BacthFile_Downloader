# yt-dlp Web UI

A clean local web interface for yt-dlp.

## Requirements

- Python 3.8+
- yt-dlp
- ffmpeg

---

## Setup (first time only)

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Make sure yt-dlp is installed
```bash
pip install yt-dlp
# or update it
pip install -U yt-dlp
```

### 3. Make sure ffmpeg is installed
- Windows: `winget install ffmpeg`  
- Mac: `brew install ffmpeg`  
- Linux: `sudo apt install ffmpeg`

---

## Run

```bash
python app.py
```

Then open your browser at: **http://localhost:5000**

---

## Features

- 🎵 Audio: MP3, AAC, FLAC, M4A, Opus, WAV, ALAC
- 🎬 Video: MP4, MKV, WebM, AVI, MOV
- 📋 Batch download (paste multiple URLs or upload .txt)
- 🖼️ Embed thumbnail as cover art
- 📝 Embed metadata (title, artist, etc.)
- 📺 Resolution picker for video (4K → 360p)
- 🔞 Cookies support for age-restricted content
- 📄 Subtitle embedding (English)
- 📁 File browser to view & re-download files
- 📊 Real-time progress log

## Supported sites

yt-dlp supports 1000+ sites including:
YouTube, Twitter/X, TikTok, Instagram, SoundCloud, Vimeo,
Twitch, Reddit, Facebook, Bilibili, Dailymotion, and many more.

---

## Downloads location

All files are saved to the `downloads/` folder inside this project.
