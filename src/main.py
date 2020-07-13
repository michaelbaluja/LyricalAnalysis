import lyricsgenius # Python-based Genius API
import pandas as pd # For organizing data to analyze
import utils # For sanitation 

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

# User input
# Authenticate with Genius API, set conditions
genius = lyricsgenius.Genius(client_access_token=input('Please enter API key: '),remove_section_headers=True)
artist_to_search = input('Enter artist to search: ')

# Create artist (max_songs = -1 in order to be able to selectively add songs later on)
## Note: Want max_songs = 0 but bug causes all songs to be searched instead of none
artist = genius.search_artist(artist_to_search, sort="title")

# Create variables to store song info in format easy to work with
df = pd.DataFrame(columns=['Song', 'Album', 'Year', 'Lyrics'])

# Create dataframe with all necessary song info
for song in artist.songs[1:]:
    date = song.year.split('-')[0] if song.year is not None else np.nan
    df = df.append({'Song':song.title, 'Album':song.album, 'Date':date, 'Lyrics':song.lyrics}, ignore_index=True)

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