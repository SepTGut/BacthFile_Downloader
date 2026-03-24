# 🎬 yt-dlp Web UI

> A clean, local web interface for **yt-dlp**  
> Download audio & video from 1000+ sites — no command line needed.

---

🌐 **Available Languages:**
&nbsp;&nbsp;🇺🇸 English (you are here)
&nbsp;&nbsp;[🇮🇩 Bahasa Indonesia](README_ID.md)
&nbsp;&nbsp;[🇷🇺 Русский](README_RU.md)
&nbsp;&nbsp;[🇨🇳 中文](README_CN.md)

---

## ✨ Features

- 🎧 Download **audio** (MP3, AAC, FLAC, M4A, Opus, WAV, ALAC)
- 🎥 Download **video** (MP4, MKV, WebM, AVI, MOV)
- 📦 Batch download — paste multiple URLs or upload a `.txt` file
- 🖼️ Embed thumbnails & metadata automatically
- 🎚️ Select resolution (4K → 360p) & audio quality
- ⚡ SponsorBlock — auto-skip sponsors, intros, outros
- 🔐 Cookie support for age-restricted / private content
- 🚦 Rate limiter to avoid getting flagged
- ⚙️ Max simultaneous downloads setting
- ✕ Cancel downloads at any time
- 📊 Real-time per-video progress + live log
- 🌙 Dark / Light mode toggle
- 🗂️ File manager with sort, delete, and re-download
- 🌐 Supports 1000+ sites: YouTube, Twitter/X, TikTok, Instagram, SoundCloud, Vimeo, and more

> All downloads are saved locally in the `downloads/` folder.

---

## 🖥️ Supported Platforms

| Platform | Script |
|----------|--------|
| 🪟 Windows | `WinOS_run.bat` |
| 🐧 Linux | `LinuxOS_run.sh` |
| 🍎 macOS | `MacOS_run.sh` |

---

## 🚀 Quick Start

### Windows
```bat
WinOS_run.bat
```

### Linux
```bash
chmod +x LinuxOS_run.sh
./LinuxOS_run.sh
```

### macOS
```bash
chmod +x MacOS_run.sh
./MacOS_run.sh
```

The script will automatically:
- ✔ Check Python installation
- ✔ Install / upgrade `yt-dlp`
- ✔ Install `ffmpeg` if missing
- ✔ Install Python dependencies
- ✔ Launch the web UI at **http://localhost:5000**

---

## ⚙️ Manual Setup

### Requirements
- Python 3.8+ → [python.org](https://python.org)
- ffmpeg → [ffmpeg.org](https://ffmpeg.org)

### Install & Run
```bash
pip install -r requirements.txt
pip install -U yt-dlp
python app.py
```
Open → **http://localhost:5000**

---

## 🧠 How to Use

1. **Paste URL(s)** — one per line, or use `ytsearch1:Song Name` to search
2. **Choose type** — Audio or Video
3. **Pick format & quality**
4. **Optional** — SponsorBlock, rate limit, subtitles, cookies
5. **Click Download** — watch real-time progress
6. **Access files** in the Downloaded Files section

---

## 📁 Project Structure

```
yt-dlp-webui/
├── app.py
├── requirements.txt
├── WinOS_run.bat
├── LinuxOS_run.sh
├── MacOS_run.sh
├── downloads/
├── cookies/
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `yt-dlp not found` | `pip install -U yt-dlp` |
| `ffmpeg not found` | Install via script or [ffmpeg.org](https://ffmpeg.org) |
| App won't open | Go to [http://localhost:5000](http://localhost:5000) manually |
| Port already in use | Change `port=5000` to `port=5001` in `app.py` |
| Format not available | Make sure ffmpeg is installed and yt-dlp is up to date |

---

## 📜 License

GPL-3.0 License — see [LICENSE](LICENSE)

---

## 🙌 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Flask](https://flask.palletsprojects.com)
- Fonts: [Syne](https://fonts.google.com/specimen/Syne) & [JetBrains Mono](https://www.jetbrains.com/lp/mono/)

---

**Enjoy downloading! 🚀**
