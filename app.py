import os
import sys
import spotipy
import time
import webbrowser
from json.decoder import JSONDecodeError
from datetime import datetime
from settings import load_credentials


class Alarm:
    def __init__(self):
        self.testSuccess = False
        self.timer = 0

    def setAlarmTime(self):
        self.alarm_time = input('Enter alarm time \'HH:MM\': ')

    def connectToSpotify(self, username, scope):
        self.username = username
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
        self.currentTime = datetime.now().strftime("%H:%M")
        if self.currentTime == self.alarm_time:
            return True

    def startMusic(self):
        spotifyObject.start_playback(self.deviceID, self.albumUri)

    def pauseMusic(self):
        spotifyObject.pause_playback(self.deviceID)

    def display(self):
        print(f'Good morning {self.username}!')
        # display album cover
        self.album = spotifyObject.current_user_playing_track()
        self.albumCover = self.album['item']['album']['images'][0]['url']
        webbrowser.open(self.albumCover)

        # While Alarm is on display the time every minute
        while True:
            self.currentTime = datetime.now().strftime("%H:%M")
            print(self.currentTime)
            time.sleep(60)
            if self.endAlarm():
                break

    def endAlarm(self):
        # end Alarm if spotify paused or 1 hour has past
        self.timer += 1
        self.isPlaying = self.album['is_playing']

        if self.isPlaying and self.timer < 60:
            return False
        else:
            return True


def getDiviceID(devices, diviceName):
    for device in devices:
        if device['name'] == deviceName:
            deviceID = device['id']
    return deviceID


if __name__ == '__main__':
    load_credentials()
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
        searchQuery = input('Enter the album you\'re looking for: ')
        searchResults = spotifyObject.search(searchQuery, 1, 0, 'album')
        albumUri = searchResults['albums']['items'][-1]['uri']

        alarm.test(deviceID, albumUri)
        if alarm.testSuccess:
            break

    # check if it is alarm time every 30 seconds
    while True:
        time.sleep(1)
        if alarm.isAlarmTime():
            alarm.startMusic()
            alarm.display()
            break
