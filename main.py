import os
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from configparser import ConfigParser

# Leer las credenciales y la ruta base del archivo de configuración
config = ConfigParser()
config.read('config.py')

client_id = config.get('Spotify', 'client_id')
client_secret = config.get('Spotify', 'client_secret')
redirect_uri = config.get('Spotify', 'redirect_uri')
username = config.get('Spotify', 'username')
base_path = config.get('General', 'base_path')

# Autorización de Spotify
credentials = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

# Obtener todas las playlists del usuario
playlists = spotify.user_playlists(username)

# Recorrer las playlists
for playlist in playlists['items']:
    playlist_name = playlist['name']
    playlist_path = os.path.join(base_path, playlist_name)

    # Crear la carpeta de la playlist si no existe
    if not os.path.exists(playlist_path):
        os.makedirs(playlist_path)

    # Obtener las canciones de la playlist
    results = spotify.user_playlist(username, playlist['id'], fields="tracks,next")
    tracks = results['tracks']
    
    # Descargar cada canción en la playlist
    while tracks:
        for item in tracks['items']:
            track = item['track']
            song_title = track['name']
            artist = track['artists'][0]['name']
            file_name = f"{song_title} ({artist}).mp3"
            file_path = os.path.join(playlist_path, file_name)

            # Descargar la canción en la ruta especificada
            os.system(f"spotify-dl --output '{file_path}' '{track['external_urls']['spotify']}'")

        # Obtener la siguiente página de resultados
        tracks = spotify.next(tracks)
