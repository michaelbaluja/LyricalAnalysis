import lyricsgenius # Python-based Genius API
import pandas as pd # For organizing data to analyze
import utils # For sanitation 
import argparse # For option specifications

# For lyrical analysis
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
from nltk.corpus import stopwords

analyser = SentimentIntensityAnalyzer()
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

# Create variables to store song info in format easy to work with
df = pd.DataFrame(columns=['Song', 'Album', 'Year', 'Lyrics'])

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
# Create and search for artist
while True:
    try:
        genius = lyricsgenius.Genius(client_access_token=key, remove_section_headers=True)
        artist = genius.search_artist(artist_to_search, sort="title")
        break
    except TypeError:
        print('Incorrect API key provided')
        key = input('Please enter API key: ')

while True:
    try:
        # Create dataframe with all necessary song info
        for song in artist.songs[1:]:
            date = song.year.split('-')[0] if song.year is not None else np.nan
            df = df.append({'Song':song.title, 'Album':song.album, 'Date':date, 'Lyrics':song.lyrics}, ignore_index=True)
    except AttributeError:
        artist_to_search = input('Please enter artist to search: ')
        artist = genius.search_artist(artist_to_search, sort="title")

# Tokenize lyrics & remove stop words
df.Lyrics = df.Lyrics.apply(word_tokenize)
df.Lyrics = df.Lyrics.apply(lambda lyrics: [word for word in lyrics if word not in stop_words])

# Add num_words for each song in order to normalize sentiment
df['n_words'] = df['Lyrics'].apply(len)
df['compound'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['compound'] for word in lyrics])) / df['n_words']
df['pos'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['pos'] for word in lyrics])) / df['n_words']
df['neu'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['neu'] for word in lyrics])) / df['n_words']
df['neg'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['neg'] for word in lyrics])) / df['n_words']

# Assign all songs w/o album to 'noalbum' (at the time of writing, no album listed on genius has the title 'noalbum', so no issue is currently anticipated)
df['Album'] = df['Album'].apply(lambda title: 'noalbum' if title is None else title)

# Get user input for which albums to analyze
albums = sorted(set(df.Album.values))
for index, album in enumerate(albums):
    print('{}: {}'.format(index, album))
albums_to_analyze = input('Input number for each album to analyze, separated by a comma: ').split(',')
albums_to_analyze = [albums[int(i)] for i in albums_to_analyze]

# Drop remixed songs 
df = utils.trim_songs(df, remix=True, unfinished=True)

# Plot albums
for album in albums_to_analyze:
    pos = df[df.Album == album].pos.sum()
    neg = df[df.Album == album].neg.sum()
    neu = df[df.Album == album].neu.sum()
    tot = pos + neg + neu
    
    plt.pie([pos / tot, neg / tot, neu / tot], autopct='%1.0f%%')
    plt.legend(['Negative', 'Positive', 'Neutral'])
    plt.title('"{}" Sentiment'.format(album))
    plt.show()
    #plt.savefig('../images/{}_pie_chart.png'.format(album))
    plt.close()