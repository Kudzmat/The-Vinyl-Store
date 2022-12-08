from app import app
from flask import render_template, request, url_for, redirect, session
from forms import AlbumSearchForm, ArtistSearchForm, PlaylistForm
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()  # load the environment variables

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_USER_ID = os.getenv('SPOTIFY_USER_ID')


SCOPE = "user-library-read user-top-read playlist-modify-public user-follow-read user-library-read " \
        "playlist-read-private playlist-modify-private"


# home page
@app.route('/')
def home_page():
    return render_template('try.html')


# route for searching for an album
@app.route('/1', methods=["GET", "POST"])
def index():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    form = AlbumSearchForm()

    if form.validate_on_submit():
        query = form.album.data

        return redirect(url_for('select_album', album_name=query))

    return render_template('home.html', form=form)


# route for searching for an artist
@app.route('/2', methods=["GET", "POST"])
def search_artist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    form = ArtistSearchForm()  # form to enter the artist's name

    if form.validate_on_submit():
        query = form.name.data

        return redirect(url_for('select_artist', artist=query))  # redirect the user to a new page

    return render_template("artist_page.html", form=form)


@app.route('/<artist>', methods=["GET", "POST"])
def select_artist(artist):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    album_names = {}  # will hold album names and images, this dictionary will prevent duplicates

    name_result = sp.search(artist, limit=1, type='artist', market='US')  # searching for the artist
    artist_display = name_result['artists']['items'][0]
    artist_name = artist_display['name']
    artist_followers = "{:,}".format(artist_display['followers']['total'])  # formatting for large numbers
    artist_genres = artist_display['genres']

    # getting top songs. We will only display the top 8 tracks on the page
    artist_info = name_result['artists']['items'][0]  # get artist ID
    artist_id = artist_info['id']
    # use ID to find top tracks
    top_tracks = sp.artist_top_tracks(artist_id)

    # search for albums using artist ID
    album_results = sp.artist_albums(artist_id=artist_id, country='US', limit=20)
    album_results = album_results['items']  # items holds all the album objects

    # this section will prevent the app from showing duplicate albums
    for album in album_results:
        if len(album_names) == 4:  # we only want to display 4 albums
            break
        else:
            if album['name'] not in album_names:
                album_names[album['name']] = album['images'][1]['url']
            else:
                pass

    return render_template('artist_display.html', name_result=name_result, artist_name=artist_name,
                           artist_followers=artist_followers, artist_genres=artist_genres, top_tracks=top_tracks,
                           album_names=album_names)


# when a user selects an album
@app.route('/display_<album_name>', methods=["GET", "POST"])
def select_album(album_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    results = sp.search(album_name, limit=1, market='US', type="album")  # taking in the album request
    album_result = results['albums']['items'][0]  # the actual album info is here
    album_id = album_result['id']  # getting the album id
    artist_name = album_result['artists'][0]['name']  # the artist's name

    # this section of the code will pull out album and track info
    album_info = sp.album(album_id)  # getting album info
    album_name = album_info['name']
    album_image = album_info['images'][1]['url']
    release_date = album_info['release_date']
    tracks = album_info['tracks']  # this section of data holds info on the actual album tracks

    return render_template('album_display.html', artist_name=artist_name, album_name=album_name,
                           release_date=release_date, album_image=album_image, tracks=tracks)


# this route will let a user try out a playlist
@app.route('/try_playlist', methods=["GET", "POST"])
def try_playlist():
    form = PlaylistForm()

    if form.validate_on_submit():
        artist_names = form.artists.data  # getting the entered artists
        artist_list = artist_names.split(',')  # getting a list of the artists entered
        session['artist_list'] = artist_list  # saving artist list for next route

        return redirect(url_for('vibe_check'))  # redirect to vibe check

    return render_template('try_playlist.html', form=form)


# route to listen to playlist
@app.route('/vibe_check/', methods=["GET", "POST"])
def vibe_check():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    playlist_name = 'Test'
    playlist_id = ''
    artists_ids = []
    tracks = []
    artist_list = session['artist_list']

    # getting the playlist we want to add the songs to
    playlists = sp.user_playlists(user=SPOTIFY_USER_ID)  # all playlists
    for item in playlists['items']:
        if item['name'] == playlist_name:
            playlist_id = item['id']

    # putting artist ids in a list
    for artist in artist_list:
        name_result = sp.search(artist, limit=1, type='artist', market='US')
        artist_info = name_result['artists']['items'][0]  # get artist ID
        artist_id = artist_info['id']
        artists_ids.append(artist_id)

    result = sp.recommendations(seed_artists=artists_ids, limit=5, country='US')  # getting 5 song recommendation
    for item in result['tracks']:
        print(item['uri'])  # getting track uris
        tracks.append(item['uri'])  # track['uri']

    sp.playlist_add_items(playlist_id=playlist_id, items=[song for song in tracks])  # adding songs

    return "CHECK SPOTIFY!!!"
