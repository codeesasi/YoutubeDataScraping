from pytubefix import YouTube
import os
import subprocess

def download_and_merge(url, save_path='.'):
    yt = YouTube(url)
    print(f"Video Title: {yt.title}")

    # Get highest resolution video-only stream (adaptive)
    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True)\
                             .order_by('resolution').desc().first()

    # Get best audio-only stream
    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True)\
                             .order_by('abr').desc().first()

    # Define temp file paths
    video_temp = os.path.join(save_path, "temp_video.mp4")
    audio_temp = os.path.join(save_path, "temp_audio.mp4")
    output_file = os.path.join(save_path, f"{yt.title}.mp4")

    # Download streams
    print("Downloading video...")
    video_stream.download(filename=video_temp)

    print("Downloading audio...")
    audio_stream.download(filename=audio_temp)

    # Merge using ffmpeg
    print("Merging video and audio...")
    merge_cmd = [
        'ffmpeg',
        '-i', video_temp,
        '-i', audio_temp,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-y',  # overwrite without asking
        output_file
    ]
    subprocess.run(merge_cmd, check=True)

    # Cleanup temp files
    os.remove(video_temp)
    os.remove(audio_temp)

    print(f"Done! Merged file saved as: {output_file}")

if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=0zwYbudzaJc'
    save_to = input("Enter save path (default is current directory): ") or '.'
    download_and_merge(video_url, save_to)
