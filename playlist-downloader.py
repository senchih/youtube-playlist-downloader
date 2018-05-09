#!/usr/bin/env python
from __future__ import division
from urllib2 import urlopen
import os, sys
import argparse
import os.path
import progressbar # pip install progressbar2
import pytube  # pip install pytube

example_playlist_url = "https://www.youtube.com/playlist?list=PLu2J4j40uuQpC0SYckwcQbGEjgOivnQmc"

def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    size = file_handle.tell()
    p = (float(size) * float(100) / float(bytes_remaining+size))
    bar.update(int(p))
    return  # do work

def get_playlist_links(playlist_url):
    page_elements = urlopen(playlist_url).readlines()
    video_elements = [el for el in page_elements if 'pl-video-title-link' in el]  # Filter out unnecessary lines
    video_urls = [v.split('href="',1)[1].split('" ',1)[0] for v in video_elements]  # Grab the video urls from the elements
    return ['http://www.youtube.com' + v for v in video_urls]

parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-p PLAYLISTURL] [-d DESTINATION][-y]')
parser.add_argument('-p', '--playlisturl', help='url of the playlist to be downloaded', default=example_playlist_url, metavar='')
parser.add_argument('-d', '--destination', help='path of directory to save videos to', default=os.path.curdir, metavar='')
parser.add_argument('-y', '--confirm', action='store_true') # -y to skip asking again
parser.add_argument('-a', '--audio', action='store_true') # -a to download the audio file, otherwise video file
args = parser.parse_args()

if os.path.exists(args.destination):
    directory_contents = [f.split('.mp4',1)[0] for f in os.listdir(args.destination) if f.endswith('.mp4')]
else:
    print('Destination directory does not exist')
    sys.exit(1)

video_urls = get_playlist_links(args.playlisturl)

if (not args.confirm):
    confirmation = raw_input('You are about to download {} videos to {}\nWould you like to continue? [Y/n] '.format(
    len(video_urls), os.path.abspath(args.destination)))    

if ((args.confirm) or (confirmation.lower() in ['y', ''])):
    for u in video_urls:
        yt = pytube.YouTube(u)
        yt.register_on_progress_callback(show_progress_bar)
        #yt_s = yt.streams.filter(file_extension='mp4')
        if (args.audio):
            yt_s = yt.streams.filter(only_audio=True)
        else:
            yt_s = yt.streams.filter(progressive=True)
        vid = yt_s.order_by('res').first() # grab the highest resolution mp4 file

        if(not vid):
            if(not yt):
                continue
            else:
                vid = pytube.YouTube(u).streams.order_by('res').first()

        print(str(vid))
        #if vid.default_filename in directory_contents:
        if (vid.default_filename and os.path.exists(args.destination + "/" +  vid.default_filename)):
            print('Skipping {}'.format(vid.default_filename))
            continue
        else:
            print('Downloading {}'.format(vid.default_filename))
            bar = progressbar.ProgressBar(maxval=100, \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
            bar.start()
            vid.download(args.destination)
            bar.update(100)
            bar.finish()

