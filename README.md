## Transmission Watch Folders
A small Python script which provides a way to automate multiple watch directories when using `TransmissionDaemon`, a CLI version of the popular Transmission torrent client.

The script runs in the background and searches the specified watch directories for torrent files, every 1 minute by default.

### Getting Started

#### Prerequisites
* `Python 2.7`
* `pip` package manager
* The ability to run the script on the same server as the transmission daemon

#### Installing
First we need to install the `transmissionrpc` library dependency.

		pip install transmissionrpc

Clone this repository and copy `main.py` and `startup.sh` to a directory where they can live permanently. Then make the startup script executable with:

		chmod +x startup.sh

You'll need to run this script on startup of your server - how you do that will depend on what OS your server is running. Google is your best friend.

#### Configuration
Edit `main.py` with your favorite text editor and find the variable definitions which are currently empty strings (`''`). Set this string to the absolute path of the directory in question. The `watch_` section contains the directories to be watched for new torrent files. The `download_dir_` section is where transmission will be told to download the files.

In the definition for the `transmissionrpc` client immediately following the path configuration variables, configure as needed - you can likely leave the port alone, but make sure you add the username and password that you use to log into Transmission RPC already.

If you'd like to change the time between directory scans, change the `time.sleep()` parameter at the very end of the script to some other number, in seconds.

Save the file. The script should now run without issues.

#### Adding Or Removing Directories
Because this is a pretty quick-and-dirty solution, you'll need to add or remove lines from the script to get the directories how you want them. To add another watch directory, you'll need to add a few things:

* The relevant `watch_` and `download_dir_` variables
* The logging print calls (assuming you want the new directory to be logged too)
* A line near the very end which adds the directories to the list, like:

		add(watch_other, download_dir_other)

Removing directories instead, is clearly the exact opposite process.

#### Other Notes
Tested on Ubuntu Server 16.04 LTS.
