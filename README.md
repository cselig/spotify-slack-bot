

# Spotify-Slack-Bot

*Bring life to your office with a collaborative playlist controlled via Slack!*


## New Features!

* Botify only responds to mentions
* Gives song info when a new song starts

## What you need

* A computer (OS X only, for now) running Spotify, with a collaborative playlist.
* Python 2 (already included with OS X), `pip` and a virtualenv tool.
* A Slack Bot integration setup and its API Key.
* A Slack channel dedicated to your playlist for the bot to broadcast messages when needed.

## Installing

First clone this repo onto a Mac with the Spotify desktop app. Use your python virtualenv tool of choice to create a Python 2 environment for the bot.

Then run the following:

```shell
pip install -r requirements.txt
```

## Configuring and Running

Make sure you have the following environment variables set:

* `SPOTIFYSLACK_SLACK_API_KEY`: your Bot integration API Key.
* `SPOTIFYSLACK_SLACK_BROADCAST_CHANNEL`: the Channel ID for your broadcast channel.

Then simply run the bot.

```shell
python spotify.py
```

## Troubleshooting
* If bot keeps failing silently, it's probably because rtm_connect() is returning false. If so, try uninstalling `websocket-client` your version of and reinstalling version `0.35` (make sure you do this with the virtual env activated).
* Make sure bot is invited to channel and channel is not private
* Make sure environment variables are set

## TO-DOs:

* Search for songs and add to the collaborative playlist.
* Add a song to the queue.
* Package this nicely for a friendlier installation and usage.

I haven't looked to see if the Spotify Applescript API currently supports things like adding songs a the playlist or queueing songs. If not, then these features would probably have to be implemented by integrating with the Spotify API.

Let me know if you're interested in adding any new features, fixing bugs, etc. Shoot me your github username and I'll grant collaborator access.

## License: MIT

Copyright © 2015 Alexandre Cisneiros - www.cisneiros.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
