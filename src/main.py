import lyricsgenius # Python-based Genius API
import pandas as pd # For organizing data to analyze
import argparse # For option specifications
import Analyzer

# For importing env variable 
import os
from dotenv import load_dotenv
load_dotenv()

# For lyrical analysis
import numpy as np
import nltk
from nltk.corpus import stopwords
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

sentiment_analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english') + [punc for punc in string.punctuation])

# Import graphing tools
import matplotlib.pyplot as plt

# Ignore handful of words that aren't stopwords but should be
import warnings
warnings.filterwarnings('ignore')

# Install necessary nltk packages in case not already installed  
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('vader_lexicon', quiet=True)

parser = argparse.ArgumentParser(description='Gather lyrical info')
parser.add_argument('--genius_key', type=str, default=None, help='key for genius api')
parser.add_argument('--artist', type=str, default=None, help='artist to search for (must be surrounded in quotes if multiple words)')
parser.add_argument('--album', type=str, default=None, help='album to search for (must be surrounded in quotes if multiple words)')
parser.add_argument('--song', type=str, default=None, help='song to search for (must be surrounded in quotes if multiple words)')
parser.add_argument('--by', type=str, default=None, help='specifies how to analyze the selected artist/song/album', choices=['album', 'artist', 'song'])
parser.add_argument('--plot', default=None, nargs='+', action='append', help='specifies how to plot the sentiment', choices=['line', 'pie'])
parser.add_argument('--remove_remix', dest='remove_remix', action='store_true')
parser.add_argument('--remove_unfinished', dest='remove_unfinished', action='store_true')
parser.add_argument('--from_cache', dest='from_cache', action='store_true')
parser.add_argument('--cache', dest='cache', action='store_true')

args = parser.parse_args()

if args.genius_key is None and os.environ.get('GENIUS_KEY') is not None:
    genius_key = os.environ.get('GENIUS_KEY')
elif args.genius_key is None:
    genius_key = input('Please enter Genius API key: ')
else: 
    genius_key = args.genius_key

# Prompt for API key if one not already present
if args.by is None and args.song is None and args.artist is not None:
    args.by = input('How would you like to analyze? (album/song): ')
elif args.by is None and args.song is not None:
    args.by = 'song'

# Access API and make sure key valid
while True:
    try:
        genius = lyricsgenius.Genius(client_access_token=genius_key, remove_section_headers=True)
        break
    except TypeError:
        print('Incorrect API key provided')
        genius_key = input('Please enter Genius API key: ')

# Create analysis onbject and analyze artist
analyzer = Analyzer.Analyzer(genius, args)
if args.artist is not None and args.song is None:
    df = analyzer.analyze_artist(args.artist, stop_words, sentiment_analyzer, by=args.by)
    by = args.by
elif args.song is not None:
    df = analyzer.analyze_song(args.song, stop_words, sentiment_analyzer, args.artist)
    by = 'song'

# Gather artists to analuze and graph them
if args.plot is not None:
    analyzer.graph(df, how=args.plot[0], by=by)