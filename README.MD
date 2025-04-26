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
pip install pytubefix