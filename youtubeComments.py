from yt_dlp import YoutubeDL
import json, bdconnect, youtubedownload
def process_comments(url):
    # URL of the YouTube video
    video_url = url
    
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

        with open(f"{safe_title}.json", "w") as outfile:
            json.dump(info, outfile)
        
        # bdconnect.insert_data_to_mongo(video_title)
        # youtubedownload.download_youtube_video(video_url)
        return video_title