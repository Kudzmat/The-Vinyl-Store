import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask
from flask import render_template, request, url_for, redirect
from forms import AlbumSearchForm

CLIENT_ID = '1e68bf09982545789b04249ccb8057fa'
CLIENT_SECRET = '19bb799a646f4c5aa89c0e582e8a5069'
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SPOTIFY_USER_ID = '31rxmn3ikrqfqxwjuoplp2u4dnk4'

scope = "user-library-read user-top-read playlist-modify-public user-follow-read user-library-read " \
        "playlist-read-private playlist-modify-private "

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

import routes

"""
albums = sp.artist_albums('7bXgB6jMjp9ATFy66eO08Z', album_type=None, country='US', limit=10)
print(albums)
return "Moving Forward!"
    """
