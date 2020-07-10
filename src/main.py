import lyricsgenius # Python-based Genius API
import pandas as pd # For organizing data to analyze
import utils # For sanitation 

# For lyrical analysis
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
from nltk.corpus import stopwords
#from nltk.stem import PorterStemmer

analyser = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

# Ignore handful of words that aren't stopwords but should be
import warnings
warnings.filterwarnings('ignore')

# Install necessary nltk packages in case not already installed
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

#ps = PorterStemmer()
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
    #year = song.year.split('-')[0]
    df = df.append({'Song':song.title, 'Album':song.album, 'Year':song.year, 'Lyrics':song.lyrics}, ignore_index=True)

# Tokenize lyrics & remove stop words
df.Lyrics = df.Lyrics.apply(word_tokenize)
df.Lyrics = df.Lyrics.apply(lambda lyrics: [word for word in lyrics if word not in stop_words])
#df.Lyrics = df.Lyrics.apply(ps.stem)

# Add num_words for each song in order to normalize sentiment
df['n_words'] = df['Lyrics'].apply(len)
df['compound'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['compound'] for word in lyrics])) / df['n_words']
df['pos'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['pos'] for word in lyrics])) / df['n_words']
df['neu'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['neu'] for word in lyrics])) / df['n_words']
df['neg'] = df['Lyrics'].apply(lambda lyrics: sum([analyser.polarity_scores(word)['neg'] for word in lyrics])) / df['n_words']