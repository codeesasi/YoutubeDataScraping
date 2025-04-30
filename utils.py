import subprocess, os
from yt_dlp import YoutubeDL
from pytubefix import YouTube
from pytubefix.contrib.search import Search, Filter
import pymongo, json
import datetime
import platform
import psutil
import requests
from tqdm import tqdm

class DockerUtils:
    def check_docker_installed():
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True, text=True)
            print("✅ Docker is installed.")
        except subprocess.CalledProcessError:
            print("❌ Docker is not installed. Please install Docker and try again.")
            exit(1)

    def pull_images():
        try:
            print("📥 Pulling Redis image...")
            subprocess.run(["docker", "pull", "redis"], check=True)
            print("✅ Redis image pulled.")

        except subprocess.CalledProcessError as e:
            print("❌ Failed to pull one of the images:", e)
            exit(1)

    def run_redis_container():
        try:
            print("🚀 Running Redis container...")
            subprocess.run([
                "docker", "run", "-d",
                "--name", "redis_server",
                "-p", "6379:6379",
                "redis"
            ], check=True)
            print("✅ Redis is running on port 6379.")
        except subprocess.CalledProcessError as e:
            print("❌ Failed to run Redis container:", e)

class Scraping:
    def get_resolutions(url):
        try:
            yt = YouTube(url)
            resolutions = []
            for stream in yt.streams:
                if stream.resolution is not None:
                    resolutions.append(stream.resolution)
            # Remove duplicate resolutions
            resolutions = list(set(resolutions))
            return sorted(resolutions, reverse=True)
        except Exception as e:
            print(f"{e}")
            return []
        
    def process_metadata(video_url: str) -> dict:
        opts = dict()
        with YoutubeDL(opts) as yt:
            info = yt.extract_info(video_url, download=False)
            res_list = Scraping.get_resolutions(video_url)
            data = {
                "Title": info.get("title"),
                "Channel": info.get("channel"),
                "Likes": info.get("like_count"),
                "views": info.get("view_count"),
                "resolutions": res_list,
                "thumbnail":info.get("thumbnail",'')
            }
            return data
    
    def Youtube_search(query:str, max_results=20, sort_by="relevance") -> list:
        try:
            filters = {'sort': sort_by}
            print(f"Searching for: {query}")
            # Set up search with multiple filters
            retries = 3
            while retries > 0:
                try:
                    s = Search(query, filters=filters)
                    # Get video results, limit to max_results
                    results = s.videos[:max_results]
                    if not results:  # Retry if results is empty
                        retries -= 1
                        if retries == 0:
                            raise ConnectionError("Failed to get results after all retries")
                        print(f"No results found, retrying... ({retries} attempts left)")
                        continue
                    break
                except ConnectionError:
                    retries -= 1
                    if retries == 0:
                        raise
                    print(f"Connection failed, retrying... ({retries} attempts left)")
            
            video_data = []
            for video in results:
                data = {
                    "Title": video.title,
                    "Channel": video.author,
                    "Views": video.views,
                    "Thumbnail": video.thumbnail_url,
                    "Upload_date": others.convert_datetime_format(video.publish_date),
                    "Video_url": video.watch_url
                    # "Dislikes": video.dislikes,  # Dislike data not reliably available now
                }
                video_data.append(data)
            return video_data
        except Exception as e:
            print(f"{e}")
            return []
    
    def download_and_merge(url, save_path='.'):
        yt = YouTube(url)
        print(f"Video Title: {yt.title}")

        # Remove or replace invalid characters for filenames
        safe_title = "".join(c for c in yt.title if c.isalnum() or c in (' ', '-', '_', '.', '(', ')')).strip()
        # Replace multiple spaces with single space
        safe_title = ' '.join(safe_title.split())
        # Limit length to avoid too long filenames
        safe_title = safe_title[:100] if len(safe_title) > 100 else safe_title
        # Get highest resolution video-only stream (adaptive)

        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True)\
                                .order_by('resolution').desc().first()

        # Get best audio-only stream
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True)\
                                .order_by('abr').desc().first()
        
        video_temp = os.path.join(save_path, "temp_video.mp4")
        audio_temp = os.path.join(save_path, "temp_audio.mp4")

        # Download streams
        print("Downloading video...")
        video_stream.download(filename=video_temp)

        print("Downloading audio...")
        audio_stream.download(filename=audio_temp)

        # Merge using ffmpeg
        print("Merging video and audio...")
        merge_cmd = [
            'ffmpeg',
            '-i', ".temp_video.mp4",
            '-i', ".temp_audio.mp4",
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-y',  # overwrite without asking
            f'{safe_title}.mp4'
        ]
        subprocess.run(merge_cmd, check=True)

        # Cleanup temp files
        os.remove(video_temp)
        os.remove(audio_temp)

        print(f"Done! Merged file saved as: {safe_title}.mp4")

    def process_comments(video_url):
        # Options for YoutubeDL to get comments
        opts = {
            "getcomments": True,
        }
        
        # Extract video information, including comments
        with YoutubeDL(opts) as yt:
            info = yt.extract_info(video_url, download=False)
            
            video_title = info.get("title")
            # Remove or replace invalid characters for filenames
            safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_', '.', '(', ')')).strip()
            # Replace multiple spaces with single space
            safe_title = ' '.join(safe_title.split())
            # Limit length to avoid too long filenames
            safe_title = safe_title[:100] if len(safe_title) > 100 else safe_title

            
            MongoDBUtils.insert_data_to_mongo(safe_title,info)
            # youtubedownload.download_youtube_video(video_url)
            return video_title

class MongoDBUtils:     
    def insert_data_to_mongo(filename:str, info:str):
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/jupitor")
        db = client.AILog
        collection = db.YoutubeCollections
        
        with open(f"{filename}.json", "w") as outfile:
            json.dump(info, outfile)

        requesting = []

        with open(f"{filename}.json") as f:
            for jsonObj in f:
                myDict = json.loads(jsonObj)
                requesting.append(pymongo.InsertOne(myDict))

        result = collection.bulk_write(requesting)
        client.close()

        print(f"Inserted {result.inserted_count} documents into the collection.")

class others:
    def convert_datetime_format(dt):
        # Convert the datetime to the desired format 'YYYY-MM-DD:HH-MM-SS'
        return dt.strftime('%Y-%m-%d:%H-%M-%S')
    
    def get_system_info():    
        # RAM Information
        ram = psutil.virtual_memory()
        ram_gb = ram.total / (1024 ** 3)

        # Disk Information
        disk = psutil.disk_usage('/')
        disk_gb = disk.total / (1024 ** 3)

        return {
            "os": platform.system(),
            "os_version": platform.release(),
            "processor": platform.processor(),
            "cpu_cores_physical": psutil.cpu_count(logical=False),
            "cpu_cores_total": psutil.cpu_count(logical=True),
            "ram_size_gb": f"{ram_gb:.2f} GB",
            "disk_size_gb": f"{disk_gb:.2f} GB"
        }
    
    def download_ollama_setup(download_folder="./downloads"):
        # Ensure download folder exists
        os.makedirs(download_folder, exist_ok=True)
        
        download_url = "https://ollama.com/download/OllamaSetup.exe"
        file_path = os.path.join(download_folder, "OllamaSetup.exe")

        print(f"Starting download from {download_url}")

        # Make the HTTP request to download the file
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        # Get the total file size for progress calculation
        total_size = int(response.headers.get('Content-Length', 0))

        # Set up tqdm to display the progress bar
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as bar:
            # Open the file in write-binary mode and write content in chunks
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))  # Update progress bar with each chunk downloaded

        print(f"✅ Download completed: {file_path}")