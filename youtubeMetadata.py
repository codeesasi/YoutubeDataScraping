from yt_dlp import YoutubeDL
from pytubefix import YouTube

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
    
def process_metadata(url):
    video_url = url
    opts = dict()
    
    with YoutubeDL(opts) as yt:
        info = yt.extract_info(video_url, download=False)
        video_title = info.get("title")
        channel = info.get("channel")
        likes = info.get("like_count")
        description = info.get("description",'')
        comments = info.get("comments",[])
        thumbnail_url = info.get("thumbnail",'')
        res_list = get_resolutions(video_url)
        data = {
            "Title": video_title,
            "Channel": channel,
            "Likes": likes,
            "views": info.get("view_count"),
            "resolutions": res_list,
            "description": description,
            "comments": comments,
            "thumbnail":thumbnail_url
        }
        return data