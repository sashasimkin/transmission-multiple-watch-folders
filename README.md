# Transmission Dir Watcher

This script watches a specified directory for new `.torrent` files and adds them to Transmission for downloading. The download directory is determined based on the folder structure of the watched directory.

This means that when you use this script to watch the directory `./torrents` which has the following structure:
```
- torrents/
  - Movies/
  - TVShows/
    - Anime/
  - Audio/
```
and configure download to `/media/`(basedir).

When you upload a `.torrent` file to `./torrents/Movies/` - the script will add it to transmission to download to `/media/Movies/`.
When you upload a `.torrent` file to `./torrents/TVShows/Anime/` - the script will add it to transmission to download to `/media/TVShows/Anime/`.
When you upload a `.torrent` file to `./torrents` - the script will add it to transmission to download to `/media/`.

When the script successfully adds a `.torrent` file to transmission, it'll delete it from the `--watch-dir` directory.
If adding fails 5 times, the file will be renamed to `{name}.failed` and an additional `{name}.traceback` will be created with the last error.

## Purpose

The purpose of this script is to automate the process of adding `.torrent` files to Transmission and organizing the downloads into a specified base directory, preserving the folder structure.

## Requirements

- Python 3.10+
- `systemd` if using the provided method of autostart

## Installation

> *Note*: It's advised to run this script as the same user as transmission-daemon.
This way the majority of settings will be picked up automatically.

1. **Clone the repository (or copy the script to your desired location):**

    ```sh
    git clone <repository-url>
    cd <project-directory>
    ```

2. **Create a virtual environment:**

    ```sh
    python3 -m venv ~/.transmission-dir-watcher-env
    source ~/.transmission-dir-watcher-env/bin/activate
    ```

3. **Install the required packages:**

    ```sh
    pip install . --force-reinstall
    ```

4. **Create a systemd user unit file:**

    Replace `your_password`, `/path/to/watch/folder`, and `/path/to/base/download/dir` with your desired locations.

    ```ini
    [Unit]
    Description=Watch directory for torrent files and add to Transmission
    After=network-online.target
    Wants=network-online.target

    [Service]
    Type=simple
    Environment=TRANSMISSION_RPC_PASSWORD=your_password
    ExecStart=%h/.transmission-dir-watcher-env/bin/transmission-dir-watcher --watch-dir /path/to/watch/folder --download-basedir /path/to/base/download/dir
    Restart=on-failure

    [Install]
    WantedBy=default.target
    ```

    Save the above content in `~/.config/systemd/user/transmission-dir-watcher.service`.

torrent-watcher --watch-dir ~/mnt/gdrive-torrents/ --download-basedir /media/data/

5. **Reload systemd and start the service:**

    ```sh
    systemctl --user daemon-reload
    systemctl --user enable --now transmission-dir-watcher.service
    # Make the service start at boot and keep running irrespective of current user login
    loginctl enable-linger
    ```

## Configuration

1. **Transmission Settings:**

    By default, the script sources Transmission settings from `~/.config/transmission-daemon/settings.json`.
    Ensure this file contains the correct settings for `rpc-bind-address`, `rpc-port`, and `rpc-username`.

    You can override the settings file location with `--transmission-settings-path` cli argument.

3. **Environment Variable:**

    Set the `TRANSMISSION_RPC_PASSWORD` environment variable to your Transmission RPC password:

    ```sh
    export TRANSMISSION_RPC_PASSWORD=your_password
    ```

## CLI Usage

Run the script with the following command (assuming you still have the python virtual environment active):

```sh
transmission-dir-watcher --watch-dir /path/to/watch/folder --download-basedir /path/to/base/download/dir
```

## Additional arguments

By default, the script scans the directory every 5 seconds. This can be changed by setting the desired number of seconds in the `--poll-interval` argument.
