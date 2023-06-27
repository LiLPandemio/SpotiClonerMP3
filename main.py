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
    playlist_name = playlist['name'].replace("/", "_")
    playlist_id = playlist['id']
    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(name,artists,name,id,external_urls))')
    playlist_name = playlist_name.replace('<3', '❤️').replace('<', 'x').replace('>', 'x')  # Reemplazar < y > en el nombre de la carpeta
    song_folder = os.path.normpath(os.path.join(output_dir, playlist_name)).replace(":", "")
    output_path = os.path.join(output_dir, playlist_name)
    linx = "cd '" + song_folder + "'\n"
    os.makedirs(output_path, exist_ok=True)
    #CREAR LA CARPETA DE LA PLAYLIST
    # Crear la carpeta si no existe de la playlist descargando
    os.makedirs(song_folder, exist_ok=True)

    archivo_m3u = os.path.join(song_folder, playlist_name + ".m3u")
    if os.path.exists(archivo_m3u):
        os.remove(archivo_m3u)
    with open(archivo_m3u, 'w') as f:
        pass
    for track in playlist_tracks['items']:
        track_title = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        track_id = track['track']['id']
        with open(archivo_m3u, "a", encoding="utf-8") as playlist_file:
            track_path = os.path.join(output_dir, playlist_name, track_title + " - " + track_artist + ".mp3")
            playlist_file.write("#EXTINF:-1," + track_artist + " - " + track_title + "\n")
            playlist_file.write("./" + track_artist + " - " + track_title + ".mp3" + "\n")


        # Crear la carpeta si no existe de la playlist descargando
        lin1 = "spotdl '" + track_title + " - " + track_artist + "'\n"
        print(song_folder + "/" + track_title)
        fullfile += linx
        fullfile += lin1
        linx = ""
    os.makedirs(song_folder, exist_ok=True)
    clean_content = fullfile.replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    clean_content = clean_content.replace('\\', '/')
    with open("temp.sh", "a", encoding='utf-8') as myfile:
        myfile.write(clean_content)