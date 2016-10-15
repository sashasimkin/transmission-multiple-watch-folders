Transmission Watch Folders
-----
Out of the box, TransmissionDaemon (CLI version of the popular torrent client) does not support multiple watch directories. This implementation attempts to remedy this. To configure the script, edit `main.py` and enter all of your watch and download folder directories. Also provide your transmission server address and other login information. Run the script and every minute the script will go through your watch directories, add any torrents it finds to the appropriate download directories, and remove the .torrent file.

Tested on Ubuntu Server 16.04 LTS

Requires Python 2.7