# 🎬 yt-dlp Web UI

> Чистый локальный веб-интерфейс для **yt-dlp**  
> Скачивайте аудио и видео с 1000+ сайтов — без командной строки.

---

🌐 **Доступные языки:**
&nbsp;&nbsp;[🇺🇸 English](README.md)
&nbsp;&nbsp;[🇮🇩 Bahasa Indonesia](README_ID.md)
&nbsp;&nbsp;🇷🇺 Русский (вы здесь)
&nbsp;&nbsp;[🇨🇳 中文](README_CN.md)

---

## ✨ Возможности

- 🎧 Загрузка **аудио** (MP3, AAC, FLAC, M4A, Opus, WAV, ALAC)
- 🎥 Загрузка **видео** (MP4, MKV, WebM, AVI, MOV)
- 📦 Пакетная загрузка — вставьте несколько URL или загрузите файл `.txt`
- 🖼️ Автоматическое встраивание обложек и метаданных
- 🎚️ Выбор разрешения (4K → 360p) и качества звука
- ⚡ SponsorBlock — автоматический пропуск рекламы, интро и аутро
- 🔐 Поддержка файлов cookie для контента с ограничением по возрасту
- 🚦 Ограничение скорости загрузки во избежание блокировок
- ⚙️ Настройка количества одновременных загрузок
- ✕ Отмена загрузки в любой момент
- 📊 Прогресс по каждому видео в реальном времени + живой лог
- 🌙 Переключение тёмной / светлой темы
- 🗂️ Менеджер файлов с сортировкой, удалением и повторной загрузкой
- 🌐 Поддержка 1000+ сайтов: YouTube, Twitter/X, TikTok, Instagram, SoundCloud, Vimeo и другие

> Все загрузки сохраняются локально в папку `downloads/`.

---

## 🖥️ Поддерживаемые платформы

| Платформа | Скрипт |
|-----------|--------|
| 🪟 Windows | `WinOS_run.bat` |
| 🐧 Linux | `LinuxOS_run.sh` |
| 🍎 macOS | `MacOS_run.sh` |

---

## 🚀 Быстрый старт

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

Скрипт автоматически:
- ✔ Проверит установку Python
- ✔ Установит / обновит `yt-dlp`
- ✔ Установит `ffmpeg`, если отсутствует
- ✔ Установит зависимости Python
- ✔ Запустит веб-интерфейс по адресу **http://localhost:5000**

---

## ⚙️ Ручная установка

### Требования
- Python 3.8+ → [python.org](https://python.org)
- ffmpeg → [ffmpeg.org](https://ffmpeg.org)

### Установка и запуск
```bash
pip install -r requirements.txt
pip install -U yt-dlp
python app.py
```
Откройте → **http://localhost:5000**

---

## 🧠 Как пользоваться

1. **Вставьте URL** — по одному в строку, или используйте `ytsearch1:Название песни` для поиска
2. **Выберите тип** — Аудио или Видео
3. **Выберите формат и качество**
4. **Опционально** — SponsorBlock, ограничение скорости, субтитры, cookie
5. **Нажмите «Скачать»** — наблюдайте за прогрессом в реальном времени
6. **Откройте файлы** в разделе загруженных файлов

---

## 📁 Структура проекта

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

## 🛠️ Устранение неполадок

| Проблема | Решение |
|----------|---------|
| `yt-dlp not found` | `pip install -U yt-dlp` |
| `ffmpeg not found` | Установите через скрипт или [ffmpeg.org](https://ffmpeg.org) |
| Приложение не открывается | Откройте [http://localhost:5000](http://localhost:5000) вручную |
| Порт уже занят | Измените `port=5000` на `port=5001` в `app.py` |
| Формат недоступен | Убедитесь, что ffmpeg установлен и yt-dlp обновлён |

---

## 📜 Лицензия

Лицензия GPL-3.0 — см. [LICENSE](LICENSE)

---

## 🙌 Благодарности

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Flask](https://flask.palletsprojects.com)
- Шрифты: [Syne](https://fonts.google.com/specimen/Syne) & [JetBrains Mono](https://www.jetbrains.com/lp/mono/)

---

**Удачных загрузок! 🚀**
