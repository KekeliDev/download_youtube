# YouTube Downloaders


This repo contains scrips for downloading YouTube videos. It creates folder for YouTube channels and playlists; this is to help you organize your files.


## Features
:one: Playlist videos downloader  ``playslist_download.py``

:two: Video download ``video_download.py``

:three: Video to mp3 ``video_to_mp3.py`` using ``FFmpeg``

:four: Playlist to mp3 ``playlist_to_mp3.py`` using ``FFmpeg``



## Setup

 * :heavy_exclamation_mark: Download [FFmpeg](https://www.ffmpeg.org/download.html) for your respective OS before using the audio features
 * Clone this repo:
 ```
 git clone https://github.com/KekeliDev/youtube_downloads.git
 ```
 * Create python virtual environment and install the packages in ``requirements.txt``  by running:

 ```
 python3 -m venv env && source env/bin/activate && pip install -r requirements.txt 
 ```
* Create download folder in the parent if not available; either ways the code will automatically create the necessary folders for you.



## Usage
 Each downloader has a avriable for link to playlist or video, replace with your link and with the env activated run the python respective script to download the video:question:

### Download playlist videos

```
python3 playslist_download.py`
```


### Download a video

```
python3 video_download.py`
```



### Get mp3 for video

```
python3 video_to_mp3.py`
```



### Get mp3 for playlist

```
python3 playlist_to_mp3.py`
```



#:heavy_exclamation_mark::heavy_exclamation_mark::heavy_exclamation_mark: DISCLAIMER :heavy_exclamation_mark::heavy_exclamation_mark::heavy_exclamation_mark:



This code is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

**Use this code at your own risk.** The authors do not guarantee that the code is free from errors or that it will work in all environments. You are responsible for testing and using this code responsibly. The authors are not responsible for any data loss, damage, or other negative consequences that may arise from using this code.




