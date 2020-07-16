import pandas as pd
import numpy as np
import lib.utils.utils as utils # For sanitation 

# For graphing
import lib.utils.grapher as gr

from nltk.tokenize import word_tokenize

class Analyzer():
    def __init__(self, genius):
        '''
        Parameters:
        - genius: (lyricsgenius.api)
            - callable api wrapper to make requests to genius.com
        '''
        self.genius = genius

    def analyze_artist(self, artist_to_search, stop_words, sentiment_analyzer, by='album'):
        '''
        Performs sentiment analysis for the provided artist based on the analysis method provided. An artist can be analyzed both by album or by song.

        Parameters:
        - artist: (str)
            - string name for the artist to analyze
        - by='album': (str)
            - specifies how to chunk the analysis being done

        Returns:
        - df: (pd.DataFrame)
            - DataFrame object containing artist sentiment information
        '''
        # Create variables to store song info in format easy to work with
        df = pd.DataFrame(columns=['Song', 'Album', 'Year', 'Lyrics'])

        while True:
            try:
                artist = self.genius.search_artist(artist_to_search, sort="title")
                # Create dataframe with all necessary song info
                for song in artist.songs:
                    date = song.year.split('-')[0] if song.year is not None else np.nan
                    df = df.append({'Song':song.title, 'Album':song.album, 'Date':date, 'Lyrics':song.lyrics}, ignore_index=True)
                break
            except AttributeError:
                artist_to_search = input('Please enter artist to search: ')
                artist = self.genius.search_artist(artist_to_search, sort="title")

        df = self.tokenize(df, stop_words)
        df = self.add_sentiment(df, sentiment_analyzer)

        # Assign all songs w/o album to 'noalbum' (at the time of writing, no album listed on genius has the title 'noalbum', so no issue is currently anticipated)
        df['Album'] = df['Album'].apply(lambda title: 'noalbum' if title is None else title)

        # Drop remixed songs 
        df = utils.trim_songs(df, remix=True, unfinished=True)
        
        return df

    def tokenize(self, df, stop_words):
        # Tokenize lyrics & remove stop words
        df.Lyrics = df.Lyrics.apply(word_tokenize)
        df.Lyrics = df.Lyrics.apply(lambda lyrics: [word for word in lyrics if word not in stop_words])

        return df

    def add_sentiment(self, df, sentiment_analyzer):
        # Add num_words for each song in order to normalize sentiment
        df['n_words'] = df['Lyrics'].apply(len)
        df['compound'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['compound'] for word in lyrics])) / df['n_words']
        df['pos'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['pos'] for word in lyrics])) / df['n_words']
        df['neu'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['neu'] for word in lyrics])) / df['n_words']
        df['neg'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['neg'] for word in lyrics])) / df['n_words']

        return df
    
    def get_albums_to_analyze(self, df):
        # Get user input for which albums to analyze
        albums = sorted(set(df.Album.values))
        for index, album in enumerate(albums):
            print('{}: {}'.format(index, album))
        self.albums_to_analyze = input('Input number for each album to analyze, separated by a comma: ').split(',')
        self.albums_to_analyze = [albums[int(i)] for i in self.albums_to_analyze]

    def graph(self, df, how=None):
        # Plot albums
        if 'pie' in how:
            for album in self.albums_to_analyze:
                gr.pieplot(df, album)