import os
import sys
import spotipy
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
from json.decoder import JSONDecodeError
from settings import load_credentials

load_credentials()
username = sys.argv[1]
scope = 'user-top-read'
number_of_top_tracks = 10

try:
    spotify_token = spotipy.util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    spotify_token = spotipy.util.prompt_for_user_token(username, scope)
spotifyObject = spotipy.Spotify(auth=spotify_token)

top_ten_tracks = spotifyObject.current_user_top_tracks(
    limit=number_of_top_tracks, time_range='short_term')

message = 'Muchacho! Here your top ten tracks of the month: \n \n'
i = 1
for item in top_ten_tracks['items']:
    song_name = item['name']
    artist = item['artists'][0]['name']
    message += f'{i}. {song_name} ({artist}) \n'
    i += 1

# get your api_id, api_hash, token
# from telegram as described above
api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
token = os.environ['TOKEN']
user_id = int(os.environ['USER_ID'])
user_hash = int(os.environ['USER_HASH'])

# your phone number
phone = '004915730207520'

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
    client.send_code_request(phone)
    # signing in the client
    client.sign_in(phone, input('Enter the code: '))

try:
    receiver = InputPeerUser(user_id, user_hash)
    # sending message using telegram client
    client.send_message(receiver, message, parse_mode='html')
except Exception as e:
    # there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
    print(e)

# disconnecting the telegram session
client.disconnect()
