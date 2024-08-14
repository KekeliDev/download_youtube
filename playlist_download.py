import os
import yt_dlp
from tqdm import tqdm

def download_playlist(playlist_url, base_output_path):
    try:
        # progress bar
        pbar = tqdm(total=100, desc="Downloading playlist", unit='%')

        # yt-dlp parameters
        ydl_opts = {
            'outtmpl': os.path.join(base_output_path, '%(uploader)s', '%(playlist_title)s', '%(title)s.%(ext)s'),
            'noplaylist': False,
            'progress_hooks': [lambda d: update_progress_bar(d, pbar)],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

        print(f"Playlist downloaded successfully!")
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
    playlist_url = "" # YouTube Playlist link
    base_output_path = "./downloads/videos"
    os.makedirs(base_output_path, exist_ok=True)
    download_playlist(playlist_url, base_output_path)
