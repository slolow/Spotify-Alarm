
**Demonstration video**
https://youtu.be/92dCJbtpm3Q

app.py:
  - This is a Spotify alarm clock
  - how to on Windows 10:
    - getting started:
      - needed: python and pip installed
      - run pip install -r requirements.txt
      - go to [Dashboard for Spotify developer](https://developer.spotify.com/dashboard/login) and login with your spotify account
      - create new app on Dashboard
      - after you have created a new app click on 'edit settings' button and add the google homepage of your country to Redirect URIs
    - run file:
      - In terminal command move to folder where you saved the file and type:
        - set SPOTIPY_CLIENT_ID=Enter your CLient Id here
        - set SPOTIPY_CLIENT_SECRET=Enter your CLient Secret here
        - set SPOTIPY_REDIRECT_URI=Enter your Redirect URL here
        - python app.py 'your Spotify username' 'the device name you want to play the music on'
        - If Running this script the first time you'll need to authorize Spotify and you'll be redirect to an URL copy that URL in the terminal command.
          This information will be saved in a file .cache-"your username" and will not be asked the next time.

spotify-app.py:
  found on https://dev.to/arvindmehairjan/how-to-play-spotify-songs-and-show-the-album-art-using-spotipy-library-and-python-5eki
