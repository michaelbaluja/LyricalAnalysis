import lyricsgenius # Python-based Genius API
import os # For reading tracklists
from utils import remove_extension, newlinestrip # Sanitization

# Authenticate with Genius API
genius = lyricsgenius.Genius(input('Please enter API key: '))

# Create artist (max_songs = 1 in order to be able to selectively add songs later on)
## Note: Want max_songs = 0 but bug causes all songs to be searched instead of none
artist = genius.search_artist("Childish Gambino", max_songs=1, sort="title")

# Read in track lists from data files, create {album : tracklist} dict pairs
track_dict = dict()
for file in os.listdir('data'):
    f = open('data/{}'.format(file), 'r')
    file = remove_extension(file)
    track_dict[file] = f.readlines()

# Sanitize tracklists by removing erraneous newline characters
for key, value in track_dict.items():
    track_dict[key] = newlinestrip(value)

# Add songs from tracklists to artist object
for album in track_dict.keys():
    for song in track_dict[album]:
        artist.add_song(genius.search_song(song, artist.name))