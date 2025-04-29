# 🎬 YouTube Tools Dashboard

A modern Python web application for YouTube video downloading, metadata extraction, comment scraping, and more. Built with **Flask**, **React (via CDN)**, **TailwindCSS**, and integrates with **MongoDB** and **Redis** for data storage and caching.

---

## ✨ Features

- 🖥️ Modern web dashboard UI (React + TailwindCSS)
- 🔍 YouTube video search and metadata extraction
- 🎥 Download highest quality video and audio streams, merge with FFmpeg
- 💬 Scrape and store YouTube comments
- 🗄️ MongoDB integration for storing video data
- 🚀 Redis support (via Docker) for caching and fast operations
- 🐳 Docker utilities for easy setup of dependencies
- 📦 Cross-platform: works on Windows, macOS, and Linux

---

## 🏗️ Project Structure

- `app.py` — Flask backend serving the dashboard and API endpoints
- `templates/index.html` — Main React+Tailwind UI (served by Flask)
- `utils.py` — Core logic for downloading, merging, scraping, and DB operations
- `requirements.txt` — Python dependencies
- `config.ini` — Configuration for API keys and MongoDB URI

---

## 🔧 Requirements

- Python 3.6+
- [pytubefix](https://pypi.org/project/pytubefix/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/) (must be installed and available in your system path)
- [MongoDB](https://www.mongodb.com/) (local or remote)
- [Redis](https://redis.io/) (can be run via Docker)

---

## 🚀 Quickstart

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/youtube-tools-dashboard.git
    cd youtube-tools-dashboard
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **(Optional) Start Redis with Docker**

    ```bash
    docker run -d --name redis_server -p 6379:6379 redis
    ```

4. **Configure MongoDB and API keys**

    Edit `config.ini` with your MongoDB URI and (optionally) OpenAI key.

5. **Run the Flask app**

    ```bash
    python app.py
    ```

6. **Open your browser**

    Visit [http://localhost:5000](http://localhost:5000) to access the dashboard.

---

## 📦 Python Dependencies

See `requirements.txt` for the full list. Key packages:

- flask
- flask-login
- flask-cors
- pytube / pytubefix
- yt_dlp
- pymongo
- redis
- tqdm

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- [pytubefix](https://github.com/nficano/pytube)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [TailwindCSS](https://tailwindcss.com/)
- [React](https://react.dev/)
- [Flask](https://flask.palletsprojects.com/)

---

## 💡 Notes

- Make sure `ffmpeg` is installed and available in your system PATH.
- For large-scale scraping or downloading, respect YouTube's Terms of Service.
- This project is for educational and personal use.