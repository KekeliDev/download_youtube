""" 
Convert YouTube video to MP3: downloads original video and uses FFmpeg to extract the audio to MP3
and deletes the original file. It also downloads the thuumbnail of the video as a cover for the mp3.
There are few bugs for embedding the thumbnail as cover, eitehr ways you will still get your mp3 file 

"""

import os
import yt_dlp
from pydub import AudioSegment
import subprocess
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

def download_video_as_mp3(video_url, base_output_path):
    try:
        
        global pbar
        pbar = tqdm(total=100, desc="Downloading video", unit='%', dynamic_ncols=True)

        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(base_output_path, '%(uploader)s', '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [lambda d: update_progress_bar(d, pbar)],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'unknown_title')
            thumbnail_url = info_dict.get('thumbnail', None)
            channel_name = info_dict.get('uploader', 'unknown_channel')
            channel_folder = os.path.join(base_output_path, channel_name)
            os.makedirs(channel_folder, exist_ok=True)
            downloaded_file = os.path.join(channel_folder, f"{video_title}.mp3")

            
            if not os.path.isfile(downloaded_file):
                raise FileNotFoundError(f"Expected MP3 file not found: {downloaded_file}")

            if thumbnail_url:
                response = requests.get(thumbnail_url)
                image = Image.open(BytesIO(response.content))
                cover_image = os.path.join(channel_folder, f"{video_title}.jpg")
                image.save(cover_image)

               
                ffmpeg_command = [
                    'ffmpeg', '-i', downloaded_file,
                    '-i', cover_image, '-c:a', 'copy', '-c:v', 'mjpeg',
                    '-map', '0:a', '-map', '1:v', '-id3v2_version', '3',
                    '-metadata', f'album={video_title}', downloaded_file
                ]
                print(f"Running FFmpeg command: {' '.join(ffmpeg_command)}")
                subprocess.run(ffmpeg_command, check=True)
                os.remove(cover_image)

            print(f"Downloaded and converted to MP3 with cover image: {downloaded_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pbar.close()

def update_progress_bar(d, pbar):
    if d['status'] == 'downloading':
        percent = d.get('download', 0) / d.get('total', 1) * 100
        pbar.n = percent
        pbar.last_print_n = percent
        pbar.update()

if __name__ == "__main__":
    video_url = "youtube video link" # YouTube video link
    base_output_path = "./downloads/audio"
    os.makedirs(base_output_path, exist_ok=True)
    download_video_as_mp3(video_url, base_output_path)


