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
        return f"An error occurred: {e}"

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=0zwYbudzaJc'
    available_resolutions = get_resolutions(video_url)
    if isinstance(available_resolutions, list):
      print("Available resolutions:")
      for res in available_resolutions:
          print(res)
    else:
        print(available_resolutions)