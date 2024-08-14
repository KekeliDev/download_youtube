"""
Convert YouTube Playlist videos to MP3: downloads original videos and uses FFmpeg to extract the audio to MP3
and deletes the original file. It also downloads the thuumbnail of the video as a cover for the mp3.
There few bugs when embedding the thumbnail as cover, either ways you will still get your mp3 file 
"""

import os
import yt_dlp
from tqdm import tqdm
import subprocess
import requests
from PIL import Image
from io import BytesIO

def download_and_convert_playlist(playlist_url, base_output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(base_output_path, '%(uploader)s', '%(playlist_title)s', '%(title)s.%(ext)s'),
            'noplaylist': False,
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=True)
            playlist_title = info_dict.get('title', 'playlist')
            uploader = info_dict.get('uploader', 'Unknown_Channel')
            playlist_folder = os.path.join(base_output_path, uploader, playlist_title)
            
            os.makedirs(playlist_folder, exist_ok=True)

            if 'entries' in info_dict:
                for entry in info_dict['entries']:
                    if entry is None:
                        continue
                    
                    video_title = entry.get('title', 'unknown_title')
                    thumbnail_url = entry.get('thumbnail', None)
                    downloaded_file = os.path.join(playlist_folder, f"{video_title}.webm")
                    mp3_file = os.path.join(playlist_folder, f"{video_title}.mp3")
                    temp_mp3_file = os.path.join(playlist_folder, f"{video_title}_temp.mp3")

                    # logging files
                    print(f"Attempting to convert file: {downloaded_file}")
                    print(f"Saving MP3 to: {mp3_file}")

                    # checking if file was successfully downloaded
                    if not os.path.exists(downloaded_file):
                        print(f"Download failed for {video_title}. The file {downloaded_file} does not exist.")
                        continue
                    
                    try:
                        # converting to MP3
                        command = ['ffmpeg', '-loglevel', 'debug', '-i', downloaded_file, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', mp3_file]
                        subprocess.run(command, check=True)

                        if thumbnail_url:
                            response = requests.get(thumbnail_url)
                            image = Image.open(BytesIO(response.content))
                            cover_image = os.path.join(playlist_folder, f"{video_title}.jpg")
                            image.save(cover_image)

                            # using video thumbnail  as cover image for mp3
                            ffmpeg_command = [
                                'ffmpeg', '-loglevel', 'debug', '-i', mp3_file,
                                '-i', cover_image, '-c:a', 'copy', '-c:v', 'mjpeg',
                                '-map', '0:a', '-map', '1:v', '-id3v2_version', '3',
                                '-metadata', f'album={video_title}', temp_mp3_file
                            ]
                            subprocess.run(ffmpeg_command, check=True)
                            
                            
                            os.replace(temp_mp3_file, mp3_file)
                            os.remove(cover_image)

                        os.remove(downloaded_file)
                        print(f"Converted {video_title} to MP3 with cover image")

                    except subprocess.CalledProcessError as e:
                        print(f"An error occurred while processing {video_title}: {e}")
                    
    except Exception as e:
        print(f"An error occurred: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        pbar.update(1)

if __name__ == "__main__":
    playlist_url = "" # YouTube Playlist link
    base_output_path = "./downloads/audio"
    os.makedirs(base_output_path, exist_ok=True)
    pbar = tqdm(total=100, desc="Downloading videos")
    download_and_convert_playlist(playlist_url, base_output_path)
    pbar.close()

