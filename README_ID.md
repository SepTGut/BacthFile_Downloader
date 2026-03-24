# 🎬 yt-dlp Web UI

> Antarmuka web lokal yang bersih untuk **yt-dlp**  
> Unduh audio & video dari 1000+ situs — tanpa perlu command line.

---

🌐 **Tersedia dalam Bahasa:**
&nbsp;&nbsp;[🇺🇸 English](README.md)
&nbsp;&nbsp;🇮🇩 Bahasa Indonesia (kamu di sini)
&nbsp;&nbsp;[🇷🇺 Русский](README_RU.md)
&nbsp;&nbsp;[🇨🇳 中文](README_CN.md)

---

## ✨ Fitur

- 🎧 Unduh **audio** (MP3, AAC, FLAC, M4A, Opus, WAV, ALAC)
- 🎥 Unduh **video** (MP4, MKV, WebM, AVI, MOV)
- 📦 Unduh massal — tempel beberapa URL atau unggah file `.txt`
- 🖼️ Sisipkan thumbnail & metadata secara otomatis
- 🎚️ Pilih resolusi (4K → 360p) & kualitas audio
- ⚡ SponsorBlock — lewati sponsor, intro, outro secara otomatis
- 🔐 Dukungan cookie untuk konten terbatas usia / privat
- 🚦 Pembatas kecepatan unduh agar tidak diblokir
- ⚙️ Pengaturan jumlah unduhan bersamaan
- ✕ Batalkan unduhan kapan saja
- 📊 Progress per-video secara real-time + log langsung
- 🌙 Tombol toggle mode Gelap / Terang
- 🗂️ Manajer file dengan sort, hapus, dan unduh ulang
- 🌐 Mendukung 1000+ situs: YouTube, Twitter/X, TikTok, Instagram, SoundCloud, Vimeo, dan lainnya

> Semua unduhan disimpan secara lokal di folder `downloads/`.

---

## 🖥️ Platform yang Didukung

| Platform | Skrip |
|----------|-------|
| 🪟 Windows | `WinOS_run.bat` |
| 🐧 Linux | `LinuxOS_run.sh` |
| 🍎 macOS | `MacOS_run.sh` |

---

## 🚀 Mulai Cepat

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

Skrip akan otomatis:
- ✔ Memeriksa instalasi Python
- ✔ Menginstal / memperbarui `yt-dlp`
- ✔ Menginstal `ffmpeg` jika belum ada
- ✔ Menginstal dependensi Python
- ✔ Membuka web UI di **http://localhost:5000**

---

## ⚙️ Instalasi Manual

### Persyaratan
- Python 3.8+ → [python.org](https://python.org)
- ffmpeg → [ffmpeg.org](https://ffmpeg.org)

### Instalasi & Jalankan
```bash
pip install -r requirements.txt
pip install -U yt-dlp
python app.py
```
Buka → **http://localhost:5000**

---

## 🧠 Cara Pakai

1. **Tempel URL** — satu per baris, atau gunakan `ytsearch1:Nama Lagu` untuk mencari
2. **Pilih jenis** — Audio atau Video
3. **Pilih format & kualitas**
4. **Opsional** — SponsorBlock, batas kecepatan, subtitle, cookie
5. **Klik Unduh** — lihat progress secara real-time
6. **Akses file** di bagian File yang Diunduh

---

## 📁 Struktur Proyek

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

## 🛠️ Pemecahan Masalah

| Masalah | Solusi |
|---------|--------|
| `yt-dlp not found` | `pip install -U yt-dlp` |
| `ffmpeg not found` | Instal lewat skrip atau [ffmpeg.org](https://ffmpeg.org) |
| Aplikasi tidak terbuka | Buka [http://localhost:5000](http://localhost:5000) secara manual |
| Port sudah digunakan | Ganti `port=5000` ke `port=5001` di `app.py` |
| Format tidak tersedia | Pastikan ffmpeg terinstal dan yt-dlp sudah diperbarui |

---

## 📜 Lisensi

Lisensi GPL-3.0 — lihat [LICENSE](LICENSE)

---

## 🙌 Kredit

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Flask](https://flask.palletsprojects.com)
- Font: [Syne](https://fonts.google.com/specimen/Syne) & [JetBrains Mono](https://www.jetbrains.com/lp/mono/)

---

**Selamat mengunduh! 🚀**
