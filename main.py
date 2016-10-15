#!/usr/bin/python

import time
import os
import os.path as path
import transmissionrpc
import datetime

# Watch directories
watch_tv = ''
watch_movie = ''
watch_music = ''

# Complete download directories
download_dir_tv = ''
download_dir_movie = ''
download_dir_music = ''

delete = True # Currently you will receive errors in the log if you do not remove the torrent file - it'll be picked up the next
              # time the script loops and will try and add the torrent again. Transmission will throw an exception because it's
              # already added.

client = transmissionrpc.Client(
    address='',
    port='',
    user='',
    password=''
    )

def add(watch_dir, download_dir):
    directory = os.listdir(watch_dir)
    files = next(os.walk(watch_dir))[2]
    if files: # files exist in directory
        for file in files:
            if file.lower().endswith('.torrent') and not file.lower().startswith('.'):
                try:
                    print '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()), "Adding torrent:", file
                    newTorrent = client.add_torrent(watch_dir + '/' + file, download_dir=download_dir)
                    time.sleep(1)
                    newTorrent.start()
                    if delete: os.remove(watch_dir + '/' + file)
                except Exception, e:
                    print '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()), "Error encountered:", str(e)
                time.sleep(1)

while True:
    print '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()), "Searching directories."
    add(watch_tv, download_dir_tv)
    add(watch_movie, download_dir_movie)
    add(watch_music, download_dir_music)
    time.sleep(60)
