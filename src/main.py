import lyricsgenius # Python-based Genius API
import pandas as pd # For organizing data to analyze
import argparse # For option specifications
import Analyzer

# For lyrical analysis
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

sentiment_analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

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
parser.add_argument('--key', type=str, default=None, help='key for genius api')
parser.add_argument('--artist', type=str, default=None, help='artist to search for (must be surrounded in quotes if multiple words)')
parser.add_argument('--album', type=str, default=None, help='album to search for (must be surrounded in quotes if multiple words)')
parser.add_argument('--song', type=str, default=None, help='song to search for (must be surrounded in quotes if multiple words)')

args = parser.parse_args()

# Request user input if args not used
if args.key == None:
    key = input('Please enter API key: ')
else: 
    key = args.key

if args.artist == None:
    artist_to_search = input('Please enter artist to search: ')
else: 
    artist_to_search = args.artist

# Access API and make sure key valid
while True:
    try:
        genius = lyricsgenius.Genius(client_access_token=key, remove_section_headers=True)
        break
    except TypeError:
        print('Incorrect API key provided')
        key = input('Please enter API key: ')

# Create analysis onbject and analyze artist
analyzer = Analyzer.Analyzer(genius)
df = analyzer.analyze_artist(artist_to_search, stop_words, sentiment_analyzer)

# Gather artists to analuze and graph them
analyzer.get_albums_to_analyze(df)
analyzer.graph(df, how=['pie'])