"""
Download the YouTube of the provided video link
"""

import os
import yt_dlp
from tqdm import tqdm

def download_video(video_url, base_output_path):
    try:
        # progressbar
        pbar = tqdm(total=100, desc="Downloading video", unit='%')

        # yt-dlp parameters
        ydl_opts = {
            'outtmpl': os.path.join(base_output_path, '%(uploader)s', '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [lambda d: update_progress_bar(d, pbar)],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print(f"Video downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pbar.close()

def update_progress_bar(d, pbar):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        pbar.n = percent
        pbar.last_print_n = percent
        pbar.update()

if __name__ == "__main__":
    video_url = "" # YouTube Video link
    base_output_path = "./downloads/videos"
    os.makedirs(base_output_path, exist_ok=True)
    download_video(video_url, base_output_path)
