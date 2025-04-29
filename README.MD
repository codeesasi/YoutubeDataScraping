# 🎥 YouTube Video Downloader & Merger (Python + pytubefix + ffmpeg)

A clean and efficient Python tool to download high-quality YouTube videos by fetching the best available **video and audio streams separately** and merging them seamlessly using **FFmpeg**.

---

## ✨ Features

- ✅ Download highest resolution video-only streams
- ✅ Download best available audio-only streams
- ✅ Merge audio + video into a single `.mp4` using `ffmpeg`
- ✅ Automatically cleans up temporary files after merging
- ✅ Cross-platform: works on Windows, macOS, and Linux
- ✅ Based on `pytubefix` (a patched fork of `pytube`)

---

## 🔧 Requirements

- Python 3.6+
- [pytubefix](https://pypi.org/project/pytubefix/)
- [ffmpeg](https://ffmpeg.org/) (must be installed and available in your system path)

### Install dependencies:

```bash

pip install flask==2.0.1
pip install flask-login==0.5.0
pip install pytube==12.1.0
pip install werkzeug==2.0.1
pip install pytubefix
pip install yt_dlp
pip install pymongo
pip install redis
pip install tqdm
pip install flask-cors==4.0.0