# 🎬 yt-dlp Web UI

> A clean, local web interface for **yt-dlp**  
> Download audio & video from 1000+ sites — no command line needed.

---

## ✨ Features

- 🎧 Download **audio** (MP3, AAC, FLAC, M4A, Opus, WAV, ALAC)
- 🎥 Download **video** (MP4, MKV, WebM, AVI, MOV)
- 📦 Batch download multiple URLs
- 🖼️ Embed thumbnails & metadata
- 🎚️ Select resolution (4K → 360p) & audio quality
- 🔐 Use cookies for restricted/private content
- 📂 Re-download saved files
- 📊 Real-time progress + logs in browser

> All downloads are saved locally in the `downloads/` folder.

---

## 👥 Who Is This For?

- 🟢 **Beginners** – No terminal needed  
- 🔵 **Advanced users** – Fast UI for yt-dlp features  
- 🟣 **Content creators** – Easy media grabbing for editing/offline use  

---

## 💡 Why This Exists

`yt-dlp` is powerful — but not beginner-friendly.

This project provides:
- 🖥️ A simple web UI
- 🔒 100% local (no third-party services)
- ⚡ Faster workflow with batch downloads
- 🌍 Cross-platform support

---

## 🖥️ Supported Platforms

- Windows 7 / 10 / 11  
- macOS (Intel & Apple Silicon)  
- Linux (Python 3.8+)  

---

## 🚀 Quick Start (One-Click)

Run the script for your OS:

### 🪟 Windows
```bash
run.bat
````

### 🐧 Linux

```bash
chmod +x run.sh
./run.sh
```

### 🍎 macOS

```bash
chmod +x run_mac.sh
./run_mac.sh
```

These scripts will:

* ✔ Check Python
* ✔ Install dependencies (`yt-dlp`, Flask)
* ✔ Install `ffmpeg` (if missing)
* ✔ Launch app at **[http://localhost:5000](http://localhost:5000)**

---

## ⚙️ Manual Setup

### 1. Install Requirements

* Python 3.8+ → [https://python.org](https://python.org)
* ffmpeg → [https://ffmpeg.org](https://ffmpeg.org)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -U yt-dlp
```

### 3. Run App

```bash
python app.py
```

Open → **[http://localhost:5000](http://localhost:5000)**

---

## 🧠 How to Use

### 1. Enter URLs

```
https://youtube.com/watch?v=...
https://twitter.com/...
```

### 2. Choose Mode

* **Audio** → format + quality
* **Video** → format + resolution

### 3. Optional

* Upload `.txt` (batch URLs)
* Upload `cookies.txt`
* Enable subtitles

### 4. Download

* View progress in real-time
* Access files in **Downloaded Files**

---

## 📁 Project Structure

```
yt-dlp-webui/
├── app.py
├── requirements.txt
├── run.bat / run.sh / run_mac.sh
├── downloads/
├── cookies/
├── templates/
└── static/
```

---

## 🛠️ Troubleshooting

### ❌ Format not available

* Ensure latest version
* Check `ffmpeg` installed

### ❌ yt-dlp not found

```bash
pip install -U yt-dlp
```

### ❌ ffmpeg not found

* Install manually or rerun script
* Restart terminal after install

### ❌ App not opening

* Go to → [http://localhost:5000](http://localhost:5000)
* Check terminal errors

### ❌ Port already in use

Change in `app.py`:

```python
app.run(port=5001)
```

---

## 📜 License

MIT License — see [LICENSE](LICENSE)

---

## 🙌 Credits

* yt-dlp
* Flask
* Fonts: Syne & JetBrains Mono

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🐛 Report issues
* 💡 Suggest features

---

**Enjoy downloading! 🚀**
