import lyricsgenius # Python-based Genius API
import os # For reading tracklists
from utils import remove_extension, newlinestrip # Sanitization

# Read in track lists from data files, create {album : tracklist} dict pairs
track_dict = dict()
for file in os.listdir('data'):
    f = open('data/{}'.format(file), 'r')
    file = remove_extension(file)
    track_dict[file] = f.readlines()

# sanitize tracklists by removing erraneous newline characters
for key, value in track_dict.items():
    track_dict[key] = newlinestrip(value)