from subprocess import check_output
from slackclient import SlackClient
import os
import re
import time
import json

from pprint import pprint

class SpotifySlackBot():
    def __init__(self, api_key, broadcast_channel, skips_needed=2):
        self.broadcast_channel = broadcast_channel
        self.sc = SlackClient(api_key)

        # Get the user list
        response = self.sc.api_call('users.list')
        self.users = json.loads(response)['members']

        # set of user ids who have requested to skip current song
        # should reset every time a new song plays
        self.skips = set()  
        self.skips_needed = skips_needed

    def command_current_song(self, event):
        data = self.run_spotify_script('current-song')
        data = data.strip().split('\n')
        data = {"id": data[0], "name": data[1], "artist": data[2]}
        message = "The current song is *%s* by *%s*." % (data['name'], data['artist'])
        
        self.sc.rtm_send_message(event['channel'], message)
        
    def command_playback_play(self, event):
        self.run_spotify_script('playback-play')
        self.sc.rtm_send_message(self.broadcast_channel, "*Resumed playback*, as requested by %s." % (self.get_username(event['user'])))
        self.sc.rtm_send_message(event['channel'], "Sure, let the music play!")

    def command_playback_pause(self, event):
        self.run_spotify_script('playback-pause')
        self.sc.rtm_send_message(self.broadcast_channel, "*Paused playback*, as requested by %s." % (self.get_username(event['user'])))
        self.sc.rtm_send_message(event['channel'], "Alright, let's have some silence for now.")

    def command_playback_skip(self, event):
        if event['user'] not in self.skips:
            self.skips.add(event['user'])
            if len(self.skips) >= self.skips_needed:
                self.run_spotify_script('playback-skip')
                self.sc.rtm_send_message(self.broadcast_channel, "*Skipping this song*")
                self.skips = set()
            else:
                self.sc.rtm_send_message(self.broadcast_channel, '%s out of %s votes needed to skip' % (len(self.skips), self.skips_needed))

        # self.sc.rtm_send_message(event['channel'], "Sure, let's listen to something else...")

    def command_help(self, event):
        self.sc.rtm_send_message(event['channel'],
                                 # "Hey, how are you?  I'm here to help you using our office playlist.\n"
                                 # "I can give you some information about what is playing right now. Just send the command:\n"
                                 "- `song`: I'll tell you which song is playing and who is the artist.\n"
                                 "\n"
                                 # "I can also control the playlist, with the following commands:\n"
                                 # "- `play`: I'll resume playback of the playlist, if it is paused.\n"
                                 # "- `pause`: I'll pause the playback of the playlist, if it is playing.\n"
                                 "- `skip`: I'll skip the current song and play another one.\n"
                                 "\n"
                                 # "*Please note:* When you give commands to control the playlist, *I'll advertise on #spotify-playlist that you asked me to do it*, just so everyone knows what is going on. Please use these only if you really need to :)"
        )

    def command_unknown(self, event):
        self.sc.rtm_send_message(event['channel'], "Hey there! I kinda didn't get what you mean, sorry. If you need, just say `help` and I can tell you how I can be of use. ;)")

    def run_spotify_script(self, *args):
        return check_output(['./spotify.applescript'] + list(args))

    def get_username(self, id):
        for user in self.users:
            if user['id'] == id:
                return '@%s' % user['name']
        return 'someone'

    def get_curr_song_info(self):
        data = self.run_spotify_script('current-song')
        data = data.strip().split('\n')
        return {"id": data[0], "name": data[1], "artist": data[2]}

    
    def run(self):
        commands = [
            ('song', self.command_current_song),
            # ('play', self.command_playback_play),
            # ('pause', self.command_playback_pause),
            ('skip|next', self.command_playback_skip),
            ('hey|help', self.command_help),
            ('.+', self.command_unknown)
        ]
        # pprint(json.loads(self.sc.api_call('channels.list')))
        # self.sc.api_call('chat.postMessage', channel=self.broadcast_channel, text='Hello World!')
        curr_song = ''
        if self.sc.rtm_connect():
            while True:
                print self.skips
                prev_song = curr_song
                curr_song = self.get_curr_song_info()['id']
                if prev_song != curr_song:
                    self.skips = set()
                events = self.sc.rtm_read()
                for event in events:
                    if event.get('type') == 'message': # and event.get('channel')[0] == 'C':
                        for (expression, function) in commands:
                            try:
                                if re.match(expression, event['text']):
                                    function(event)
                                    break
                            except:
                                pass
                time.sleep(1)

if __name__ == '__main__':
    bot = SpotifySlackBot(os.environ.get('SPOTIFYSLACK_SLACK_API_KEY'), os.environ.get('SPOTIFYSLACK_SLACK_BROADCAST_CHANNEL'))
    bot.run()
