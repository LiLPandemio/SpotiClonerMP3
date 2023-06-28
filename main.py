import configparser                         # Para leer el archivo config.ini
import os                                   # Manipulacion de directorios
import spotipy                              # Autenticacion en spotify
from spotipy.oauth2 import SpotifyOAuth     # Para gestionar el oauth de spotify

"""
TODO: Comprobar si la cancion existe. En ese caso no hay que añadirla al script. Esto acelera mucho el proceso ya que spotdl es lento comprobando esto.
"""

# Leer config
config = configparser.ConfigParser()
config.read('config.ini')

# Tratar la config
client_id = config.get('spotify', 'client_id')
client_secret = config.get('spotify', 'client_secret')
redirect_uri = config.get('spotify', 'redirect_uri')
output_dir = config.get('download', 'output_dir')

# Autenticación con Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-read-private'))

# Obtener la lista de playlists del usuario
playlists = sp.current_user_playlists()

# Descargar cada canción de cada playlist en la biblioteca
tempsh_file = f"cd {output_dir}\n"                        # Aqui se guardara el contenido del archivo temp.sh. Se añade un cd a la direccion para descargar luego ahi la musica con bash

# Bucle para recorrer playlists
for playlist in playlists['items']:
    
    # Acomodar los valores actuales en variables
    playlist_name = playlist['name']        # Nombre de la playlist para no trabajar sobre el array playlist
    playlist_id = playlist['id']            # ID de la playlist
    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(name,artists,name,id,external_urls))')       # Obtener la lista de las canciones de la playlist en un array
    playlist_name_safe = playlist_name.replace("<3", "❤️").replace("/", "_").replace('<', 'x').replace('>', 'x')            # Reemplazar < y > en el nombre de la carpeta    
    
    # Crear directorio de salida en caso de que no exista
    os.makedirs(output_dir, exist_ok=True)

    # Archivo de playlist m3u. Este archivo tiene el titulo de la playlist y su contenido
    archivo_m3u = os.path.join(output_dir, playlist_name_safe + ".m3u") # Genera el path al archivo m3u de la playlist.

    # Si existe se elimina para actualizarse bien
    if os.path.exists(archivo_m3u):                                     # Comprueba si existe el archivo m3u
        os.remove(archivo_m3u)                                          # Elimina el archivo m3u actual (Si existe)
    
    # Crea el archivo m3u en blanco y mete la cabecera
    with open(archivo_m3u, 'w') as f:                                   # Crea el archivo m3u nuevo
        f.write("#EXTM3U \n")                                              # Encabezado del archivo m3u
        f.write(f"#PLAYLIST:{playlist_name} \n")                           # Encabezado del archivo m3u (Titulo)

    # Bucle para recorrer canciones en la playlist actual
    for track in playlist_tracks['items']:                              # Por cada track en playlist

        # Acomodar los valores actuales en variables
        track_title = track['track']['name']                                # Titulo de la cancion
        track_artist = track['track']['artists'][0]['name']                 # Artista principal de la cancion
        
        # Añadir a la playlist las canciones en formato EXTINF
        with open(archivo_m3u, "a", encoding="utf-8") as playlist_file:     # Añadir al archivo m3u la cancion
            playlist_file.write("#EXTINF:-1," + track_artist + " - " + track_title + "\n") # Especifica el titulo
            playlist_file.write("./" + track_artist + " - " + track_title + ".mp3" + "\n") # Especifica el path

        # Añadir al script de descarga la cancion en el formato del comando.
        nextline = "spotdl '" + track_title + " - " + track_artist + "'\n"  # La linea en el script tempsh
        print(output_dir + " | " + nextline)                                # Muestra por pantalla el comando generado
        tempsh_file += nextline                                             # Añade la linea al archivo tempsh
        #Fin del bucle
        #Fin del bucle

    #Limpieza de simbolos en titulos de canciones y escritura del script
    clean_content = tempsh_file.replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('\\', '/').replace("//", "/") # Elimina caracteres prohibidos de los filenames
    with open("temp.sh", "a", encoding='utf-8') as myfile: # Añadir al archivo de descargas
        myfile.write(clean_content)
