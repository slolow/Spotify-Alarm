import os
import sys
import spotipy
import time
from json.decoder import JSONDecodeError
from datetime import datetime


class Alarm:
    def __init__(self):
        self.testSuccess = False

    def setAlarmTime(self):
        self.alarm_time = input('Enter alarm time \'HH:MM\': ')

    def connectToSpotify(self, username, scope):
        try:
            self.token = spotipy.util.prompt_for_user_token(username, scope)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            self.token = spotipy.util.prompt_for_user_token(username, scope)
        return self.token

    # test if the right album was found
    def test(self, deviceID, albumUri):
        self.deviceID = deviceID
        self.albumUri = albumUri
        self.startMusic()
        # check test
        self.rightAlbum = input('Is the right album playing? y or n? ')
        if self.rightAlbum == 'y':
            self.pauseMusic()
            print(f'You\'re Alarm will rise at {self.alarm_time}. Sleep well!')
            self.testSuccess = True

    def isAlarmTime(self):
        self.current_time = datetime.now().strftime("%H:%M")
        if self.current_time == self.alarm_time:
            return True

    def startMusic(self):
        spotifyObject.start_playback(self.deviceID, self.albumUri)

    def pauseMusic(self):
        spotifyObject.pause_playback(self.deviceID)


def getDiviceID(devices, diviceName):
    for device in devices:
        if device['name'] == deviceName:
            deviceID = device['id']
    return deviceID


# Get the username and devicename from terminal
username = sys.argv[1]
deviceName = sys.argv[2]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# set alarm
alarm = Alarm()
alarm.setAlarmTime()
token = alarm.connectToSpotify(username, scope)

# search for the device id to play the music on
spotifyObject = spotipy.Spotify(auth=token)
devices = spotifyObject.devices()['devices']
deviceID = getDiviceID(devices, deviceName)

# search for an album as long as the user found the right one
while True:
    # search for an album
    searchQuery = input('Enter the album you\'re looking for: ' )
    searchResults = spotifyObject.search(searchQuery,1,0,'album')
    albumUri = searchResults['albums']['items'][-1]['uri']

    alarm.test(deviceID, albumUri)
    if alarm.testSuccess:
        break

# check if it is alarm time
while True:
    time.sleep(30)
    if alarm.isAlarmTime():
        alarm.startMusic()
        break
