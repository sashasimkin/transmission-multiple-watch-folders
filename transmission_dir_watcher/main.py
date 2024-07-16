import os
import time
import json
import logging
import traceback
import argparse

import transmission_rpc


logging.basicConfig(level=logging.INFO)

_FAILED_TORRENTS = {}

def load_transmission_settings(settings_path):
    settings_path = os.path.expanduser(settings_path)
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    return settings

def find_torrents(folder):
    torrent_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.torrent'):
                torrent_files.append(os.path.join(root, file))
    return torrent_files

def add_torrents_to_transmission(tc, torrent_path, watch_folder, base_download_dir):
    global _FAILED_TORRENTS

    relative_path = os.path.relpath(torrent_path, watch_folder)
    download_subdir = os.path.dirname(relative_path)
    download_dir = os.path.join(base_download_dir, download_subdir)
    logging.info(f'Adding torrent: {torrent_path} to download directory: {download_dir}')
    try:
        tc.add_torrent(torrent_path, download_dir=download_dir)
    except Exception as e:
        _FAILED_TORRENTS.setdefault(torrent_path, 0)
        _FAILED_TORRENTS[torrent_path] += 1
        if _FAILED_TORRENTS[torrent_path] > 5:
            logging.exception(f"Adding torrent failed {_FAILED_TORRENTS[torrent_path]} time(s), setting file to be ignored: {torrent_path}")
            del _FAILED_TORRENTS[torrent_path]
            os.rename(torrent_path, f'{torrent_path}.failed')
            with open(f'{torrent_path}.traceback', 'w') as logf:
                traceback.print_exc(file=logf)
        else:
            logging.exception(f"Adding torrent failed {_FAILED_TORRENTS[torrent_path]} time(s), will retry: {torrent_path}")
    else:
        logging.info(f'Removed torrent file: {torrent_path}')
        os.remove(torrent_path)

def watch_folder(folder, base_download_dir, tc, poll_interval):
    logging.info(f'Starting to watch folder: {folder}')
    while True:
        torrent_files = find_torrents(folder)
        for torrent_file in torrent_files:
            add_torrents_to_transmission(tc, torrent_file, folder, base_download_dir)
        time.sleep(poll_interval)

def main():
    parser = argparse.ArgumentParser(description='Watch a directory and add .torrent files to Transmission.')
    parser.add_argument('--watch-dir', required=True, help='The directory to watch for .torrent files.')
    parser.add_argument('--download-basedir', required=True, help='The base directory for downloading torrents.')
    parser.add_argument('--transmission-settings-path', default='~/.config/transmission-daemon/settings.json', help='The path to the Transmission settings file.')
    parser.add_argument('--poll-interval', type=int, default=5, help='The polling interval in seconds.')

    args = parser.parse_args()

    settings = load_transmission_settings(args.transmission_settings_path)
    transmission_host = settings.get('rpc-bind-address', 'localhost')
    transmission_port = settings.get('rpc-port', 9091)
    transmission_user = settings.get('rpc-username')
    transmission_password = os.getenv('TRANSMISSION_RPC_PASSWORD')

    if not transmission_password:
        raise EnvironmentError('TRANSMISSION_RPC_PASSWORD environment variable not set.')

    tc = transmission_rpc.Client(
        host=transmission_host,
        port=transmission_port,
        username=transmission_user,
        password=transmission_password
    )

    watch_folder(args.watch_dir, args.download_basedir, tc, args.poll_interval)

if __name__ == "__main__":
    main()
