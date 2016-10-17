#!/usr/bin/python

import time
import os, sys
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

client = transmissionrpc.Client(
    address='127.0.0.1',
    port='9091',
    user='',
    password=''
    )

# Logging
log = open('./log.txt', 'a')
timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
print >> log, timestamp +  ' ' + 'Started watch script.'
print >> log, 'Current watch directories:'
print >> log, '    TV: ' + watch_tv
print >> log, 'Movies: ' + watch_movie
print >> log, ' Music: ' + watch_music
print >> log, 'Current download directories:'
print >> log, '    TV: ' + download_dir_tv
print >> log, 'Movies: ' + download_dir_movie
print >> log, ' Music: ' + download_dir_music
log.close()

def add(watch_dir, download_dir):
    directory = os.listdir(watch_dir)
    files = next(os.walk(watch_dir))[2]
    if files: # files exist in directory
        for file in files:
            if file.lower().endswith('.torrent') and not file.lower().startswith('.'):
            log = open('./log.txt', 'a')
            timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())

                try:
            print >> log, timestamp + ' ' + 'Adding torrent: ' + file
                    newTorrent = client.add_torrent(watch_dir + '/' + file, download_dir=download_dir)
                    time.sleep(1)
                    newTorrent.start()
                    os.remove(watch_dir + '/' + file)
                except Exception, e:
            print >> log, timestamp + ' ' + 'Error encountered: ' + str(e)

        log.close()
                time.sleep(1)

while True:
    log = open('./log.txt', 'a')
    timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
    print >> log, timestamp + ' ' + 'Searching directories.'
    add(watch_tv, download_dir_tv)
    add(watch_movie, download_dir_movie)
    add(watch_music, download_dir_music)
    time.sleep(60)
