from app import app
from flask import render_template, request, url_for, redirect
from forms import AlbumSearchForm, ArtistSearchForm
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '1e68bf09982545789b04249ccb8057fa'
CLIENT_SECRET = '19bb799a646f4c5aa89c0e582e8a5069'
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SPOTIFY_USER_ID = '31rxmn3ikrqfqxwjuoplp2u4dnk4'

SCOPE = "user-library-read user-top-read playlist-modify-public user-follow-read user-library-read " \
        "playlist-read-private playlist-modify-private "


# home page
@app.route('/')
def home_page():
    return render_template('album_page.html')


# route for searching for an album
@app.route('/1', methods=["GET", "POST"])
def index():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    form = AlbumSearchForm()
    artist_name = None
    album_name = None
    release_date = None
    tracks = None
    album_image = None

    if form.validate_on_submit():
        query = form.album.data
        results = sp.search(query, limit=1, market='US', type="album")  # taking in the album request

        album_result = results['albums']['items'][0]  # the actual album info is here
        album_id = album_result['id']  # getting the album id
        artist_name = album_result['artists'][0]['name']  # the artist's name

        # this section of the code will pull out album and track info
        album_info = sp.album(album_id)  # getting album info
        album_name = album_info['name']
        album_image = album_info['images'][1]['url']
        release_date = album_info['release_date']
        tracks = album_info['tracks']  # this section of data holds info on the actual album tracks

    return render_template('home.html', form=form, artist_name=artist_name, album_name=album_name,
                           release_date=release_date, album_image=album_image, tracks=tracks)


# route for searching for an artist
@app.route('/2', methods=["GET", "POST"])
def search_artist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    form = ArtistSearchForm()
    query = ""  # will take input from search query
    name_result = ""  # result from search query
    artist_name = ""
    artist_followers = ""
    artist_genres = []

    artist_id = ""  # will hold the artist id
    artist_info = ""  # will hold artist information
    top_tracks = ""  # will hold the artist's top tracks

    if form.validate_on_submit():
        query = form.name.data
        name_result = sp.search(query, limit=1, type='artist', market='US')
        artist_display = name_result['artists']['items'][0]
        artist_name = artist_display['name']
        artist_followers = "{:,}".format(artist_display['followers']['total'])  # formatting for large numbers
        artist_genres = artist_display['genres']

        # getting top 5 songs
        artist_info = name_result['artists']['items'][0]  # get artist ID
        artist_id = artist_info['id']
        # use ID to find top tracks
        top_tracks = sp.artist_top_tracks(artist_id)

    return render_template("artist_page.html", form=form, name_result=name_result, artist_name=artist_name,
                           artist_followers=artist_followers, artist_genres=artist_genres, top_tracks=top_tracks)
