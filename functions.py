import os

def song_exists(path, title, artist):
    for file_name in os.listdir(path):
        if title in file_name and artist in file_name:
            return True
    return False