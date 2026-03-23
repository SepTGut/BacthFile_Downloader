# yt-dlp Web UI

A clean, local web interface for [yt-dlp](https://github.com/yt-dlp/yt-dlp).  
Download audio or video from 1000+ sites with a few clicks – no command line needed.

---

## 1. What – The Project

This is a **Flask‑based web application** that provides a graphical front‑end for `yt-dlp`, a powerful downloader supporting YouTube, Twitter, TikTok, Instagram, SoundCloud, and hundreds more.  
It allows you to:

- Download **audio** (MP3, AAC, FLAC, M4A, Opus, WAV, ALAC) or **video** (MP4, MKV, WebM, AVI, MOV)  
- Batch download multiple URLs at once  
- Embed thumbnails and metadata (artist, title, etc.)  
- Select video resolution (4K → 360p) and audio quality  
- Use cookies for age‑restricted or private content  
- View and re‑download previously saved files  
- See real‑time progress and logs in your browser  

All downloads are stored locally in the `downloads/` folder.

---

## 2. Who – For Whom

This tool is for anyone who wants to download media from supported sites without using the terminal.  
- **Beginners**: no command‑line experience needed – just a browser.  
- **Advanced users**: quick access to yt‑dlp’s features with a clean UI and batch processing.  
- **Content creators**: grab audio/video for editing, archiving, or offline viewing.

---

## 3. Why – Motivation

The command‑line interface of yt‑dlp is powerful but can be intimidating. This project wraps it in a friendly, local web UI, making it accessible to everyone. It also:

- Avoids relying on third‑party online services – everything runs on your machine.  
- Provides a consistent interface across Windows, macOS, and Linux.  
- Saves time with batch downloads and automatic format selection.

---

## 4. When – Availability

The project is ready to use now. Once installed, you can start it anytime – it runs locally on your computer.  
There’s no need for an internet connection beyond accessing the source sites.

---

## 5. Where – Installation & Environment

The app runs on your own machine. All files stay on your computer; nothing is sent to external servers.

### Supported Platforms
- Windows (7/10/11)  
- macOS (Intel/Apple Silicon)  
- Linux (any distribution with Python 3.8+)

---

## 6. How – Setup & Usage

### 6.1 Requirements
- Python 3.8+ (must be installed)  
- ffmpeg (for audio extraction and video merging)  
- yt-dlp (installed via pip)  
- Flask (installed via pip)

The **one‑click run scripts** (provided below) automatically check for and install missing dependencies.

---

### 6.2 One‑Click Run Scripts

We supply three scripts – one for each operating system. They will:

1. Verify Python is installed.  
2. Install/update `yt-dlp` and `Flask`.  
3. Attempt to install `ffmpeg` if missing (via winget/Homebrew/apt).  
4. Start the Flask server and open `http://localhost:5000` in your browser.

#### Windows (`run.bat`)
Double‑click `run.bat` in the project folder.  
*Note: Python must be installed separately beforehand.*

#### Linux (`run.sh`)
Open a terminal in the project folder and run:
```bash
chmod +x run.sh
./run.sh
```

#### macOS (`run_mac.sh`)
Open a terminal in the project folder and run:
```bash
chmod +x run_mac.sh
./run_mac.sh
```
*Requires Homebrew (install from https://brew.sh if not present).*

If the scripts fail, follow the manual steps below.

---

### 6.3 Manual Setup (Step‑by‑Step)

1. **Install Python 3.8+** from [python.org](https://python.org). Ensure `python` is in your PATH.

2. **Install ffmpeg**  
   - **Windows**: `winget install ffmpeg` (or download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH)  
   - **macOS**: `brew install ffmpeg`  
   - **Linux**: `sudo apt install ffmpeg` (or your package manager)

3. **Install Python dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
   This installs Flask.

4. **Install/upgrade yt-dlp**  
   ```bash
   pip install -U yt-dlp
   ```

5. **Run the app**  
   ```bash
   python app.py
   ```
   Then open your browser at **http://localhost:5000**.

---

### 6.4 How to Use the Web UI

1. **Enter URLs** – one per line.  
   Example:  
   ```
   https://youtube.com/watch?v=...
   https://twitter.com/...
   https://soundcloud.com/...
   ```

2. **Choose Type**:  
   - **Audio**: select format (MP3, AAC, FLAC, M4A, Opus, WAV, ALAC) and quality (0 = best, 9 = smallest).  
   - **Video**: select format (MP4, MKV, WebM, AVI, MOV) and resolution (best / 4K / 1440p / 1080p / …).

3. **Optional**:  
   - Upload a batch `.txt` file containing one URL per line.  
   - Upload a `cookies.txt` file for age‑restricted or private content (exported via browser extension like “Get cookies.txt”).  
   - Check “Embed subtitles” to download and embed English subtitles.

4. Click **Download**. The progress bar and live log will show the process.  
   - When finished, the file appears in the **Downloaded Files** list.  
   - Click “Save” to download the file again from the UI.

5. To start another download, click **New Download**.

---

### 6.5 Project Structure

```
yt-dlp-webui/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies (Flask)
├── run.bat                 # Windows one‑click script
├── run.sh                  # Linux one‑click script
├── run_mac.sh              # macOS one‑click script
├── README.md               # This file
├── downloads/              # Saved media files (created automatically)
├── cookies/                # Uploaded cookie files (created automatically)
├── templates/
│   └── index.html          # Frontend HTML
└── static/
    ├── style.css           # Styles
    └── app.js              # Frontend logic
```

---

## 7. Troubleshooting

### “Requested format is not available” (video)
- **Fixed in this version** – the format selector now picks the best video+audio streams without container restrictions, then merges them to your chosen format using `--merge-output-format`.  
- Ensure you have the latest `app.py` and that `ffmpeg` is installed and in PATH.

### yt-dlp not found
- Run `pip install -U yt-dlp` again.  
- On Windows, verify that the Python Scripts folder (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts`) is in your PATH.

### ffmpeg not found
- Install ffmpeg manually (see above) or let the run script try to install it.  
- After installation, restart your terminal / command prompt.

### The app doesn’t open automatically
- Manually go to `http://localhost:5000` in your browser.  
- Check the terminal output for errors – e.g., if port 5000 is already in use, change the port in `app.py` (last line) and update the scripts accordingly.

### Port 5000 is already in use
- Edit `app.py` and change the last line to:  
  ```python
  app.run(debug=False, port=5001)
  ```
- Then open `http://localhost:5001`.

### Cookies not working
- Make sure the cookie file is in the correct Netscape format (exported by an extension).  
- The file must be a `.txt` file.

---

## 8. License

MIT License – see the [LICENSE](LICENSE) file for details.

## 9. Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) – the core downloader  
- [Flask](https://flask.palletsprojects.com/) – lightweight web framework  
- Fonts: [Syne](https://fonts.google.com/specimen/Syne) & [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono)

---

**Enjoy!** If you have any issues or suggestions, feel free to open an issue on GitHub.
```

