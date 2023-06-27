import configparser
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config.get('spotify', 'client_id')
client_secret = config.get('spotify', 'client_secret')
redirect_uri = config.get('spotify', 'redirect_uri')
output_dir = config.get('download', 'output_dir')

# Autenticación con Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-read-private'))

# Obtener la lista de playlists del usuario
playlists = sp.current_user_playlists()

# Descargar cada canción de cada playlist en la biblioteca
for playlist in playlists['items']:
    fullfile = ""
    playlist_name = playlist['name']
    playlist_id = playlist['id']
    output_path = os.path.join(output_dir, playlist_name)
    os.makedirs(output_path, exist_ok=True)
    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(name,artists,name,id,external_urls))')
    song_folder = os.path.normpath(os.path.join(output_dir, playlist_name)).replace(":", "")
    linx="cd \"" + song_folder + "\"\n"
    for track in playlist_tracks['items']:
        track_title = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        track_id = track['track']['id']
        
        #Crear la carpeta si no existe de la playlist descargando
        lin1="spotdl \""+ track_title + " - " + track_artist +"\"\n" 
        print(song_folder + "/" + track_title)
        fullfile += linx
        fullfile += lin1 
        linx=""
    os.makedirs(song_folder, exist_ok=True)
    with open("temp.ps1", "a", encoding='utf-16LE') as myfile:
        myfile.write(fullfile)
    fullfile = ""