from yt_dlp import YoutubeDL
import json, bdconnect, youtubedownload

# URL of the YouTube video
video_url = "https://www.youtube.com/watch?v=Mr09i79DaNg"
  
# Options for YoutubeDL to get comments
opts = {
    "getcomments": True,
}
  
# Extract video information, including comments
with YoutubeDL(opts) as yt:
    info = yt.extract_info(video_url, download=False)
      
    video_title = info.get("title")

    with open(f"{video_title}.json", "w") as outfile:
        json.dump(info, outfile)
    
    bdconnect.insert_data_to_mongo(video_title)
    youtubedownload.download_youtube_video(video_url)