# 🎬 yt-dlp Web UI

> 简洁的本地 **yt-dlp** 网页界面  
> 从 1000+ 个网站下载音频和视频 — 无需命令行。

---

🌐 **可用语言：**
&nbsp;&nbsp;[🇺🇸 English](README.md)
&nbsp;&nbsp;[🇮🇩 Bahasa Indonesia](README_ID.md)
&nbsp;&nbsp;[🇷🇺 Русский](README_RU.md)
&nbsp;&nbsp;🇨🇳 中文（当前页面）

---

## ✨ 功能特性

- 🎧 下载**音频**（MP3、AAC、FLAC、M4A、Opus、WAV、ALAC）
- 🎥 下载**视频**（MP4、MKV、WebM、AVI、MOV）
- 📦 批量下载 — 粘贴多个 URL 或上传 `.txt` 文件
- 🖼️ 自动嵌入封面图片和元数据
- 🎚️ 选择分辨率（4K → 360p）和音频质量
- ⚡ SponsorBlock — 自动跳过赞助商、片头、片尾
- 🔐 支持 Cookie，可下载年龄限制或私有内容
- 🚦 限速功能，避免被封禁
- ⚙️ 可设置最大同时下载数
- ✕ 随时取消下载
- 📊 实时逐视频进度 + 实时日志
- 🌙 深色 / 浅色模式切换
- 🗂️ 文件管理器，支持排序、删除和重新下载
- 🌐 支持 1000+ 网站：YouTube、Twitter/X、TikTok、Instagram、SoundCloud、Vimeo 等

> 所有下载文件保存在本地 `downloads/` 文件夹中。

---

## 🖥️ 支持平台

| 平台 | 脚本 |
|------|------|
| 🪟 Windows | `WinOS_run.bat` |
| 🐧 Linux | `LinuxOS_run.sh` |
| 🍎 macOS | `MacOS_run.sh` |

---

## 🚀 快速开始

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

脚本将自动：
- ✔ 检查 Python 安装情况
- ✔ 安装 / 升级 `yt-dlp`
- ✔ 若缺少则安装 `ffmpeg`
- ✔ 安装 Python 依赖
- ✔ 在 **http://localhost:5000** 启动网页界面

---

## ⚙️ 手动安装

### 依赖要求
- Python 3.8+ → [python.org](https://python.org)
- ffmpeg → [ffmpeg.org](https://ffmpeg.org)

### 安装与运行
```bash
pip install -r requirements.txt
pip install -U yt-dlp
python app.py
```
打开 → **http://localhost:5000**

---

## 🧠 使用方法

1. **粘贴 URL** — 每行一个，或使用 `ytsearch1:歌曲名称` 搜索
2. **选择类型** — 音频或视频
3. **选择格式和质量**
4. **可选** — SponsorBlock、限速、字幕、Cookie
5. **点击下载** — 实时查看进度
6. **在已下载文件区域访问文件**

---

## 📁 项目结构

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

## 🛠️ 故障排除

| 问题 | 解决方法 |
|------|----------|
| `yt-dlp not found` | `pip install -U yt-dlp` |
| `ffmpeg not found` | 通过脚本安装或访问 [ffmpeg.org](https://ffmpeg.org) |
| 应用无法打开 | 手动访问 [http://localhost:5000](http://localhost:5000) |
| 端口已被占用 | 将 `app.py` 中的 `port=5000` 改为 `port=5001` |
| 格式不可用 | 确保已安装 ffmpeg 且 yt-dlp 为最新版本 |

---

## 📜 许可证

GPL-3.0 许可证 — 详见 [LICENSE](LICENSE)

---

## 🙌 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Flask](https://flask.palletsprojects.com)
- 字体：[Syne](https://fonts.google.com/specimen/Syne) & [JetBrains Mono](https://www.jetbrains.com/lp/mono/)

---

**祝下载愉快！🚀**
