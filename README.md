# youtube-playlist-downloader
A Python CLI utility to download an entire playlist from YouTube.
By default it downloads the videos from a youtube playlist.

To run, clone this repository into an empty directory:
 `git clone https://github.com/senchih/youtube-playlist-downloader.git`
 
Then install the dependencies:
 `pip install pytube`
 `pip install progressbar`
 
Finally run the script:
 `python playlist-downloader.py`
 
Specify a playlist url:
 `python playlist-downloader.py -p https://www.youtube.com/playlist?list=UUi9wbhjrZ4nTIHgZ0r31v8g`
 
Destination directory:
 `python playlist-downloader.py -d ~/Desktop/`

Download the audio only:
 `python playlist-downloader.py -a`

Download the files without checking videos number:
 `python playlist-downloader.py -y`
 
The script checks if the videos from the playlist are already in the destination directory.
This means you can re-run the script and only download the newly uploaded content.

(This is forked from https://github.com/svass/youtube-playlist-downloader.git)
