import pandas as pd
import numpy as np
import lib.utils.utils as utils # For sanitation 
import string

# For graphing
import lib.utils.grapher as gr

from nltk.tokenize import word_tokenize

class Analyzer():
    def __init__(self, genius, args):
        '''
        Parameters:
        - genius: (lyricsgenius.api)
            - callable api wrapper to make requests to genius.com
        '''
        self.genius = genius
        self.remove_remix = args.remove_remix
        self.remove_unfinished = args.remove_unfinished

    def analyze_artist(self, artist_to_search, stop_words, sentiment_analyzer, by='album'):
        '''
        Performs sentiment analysis for the provided artist based on the analysis method provided. An artist can be analyzed both by album or by song.

        Parameters:
        - artist: (str)
            - string name for the artist to analyze
        - by='album': (str)
            - specifies how to chunk the analysis being done.

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
        df = utils.trim_songs(df, remix=self.remove_remix, unfinished=self.remove_unfinished)

        # Gather songs based on specified method
        if by == 'album':
            self.get_albums_to_analyze(df)
        elif by == 'song':
            self.get_songs_to_analyze(df)

        return df

    def tokenize(self, df, stop_words):
        # Tokenize lyrics & remove stop words
        df.Lyrics = df.Lyrics.apply(word_tokenize)
        df.Lyrics = df.Lyrics.apply(lambda lyrics: [word for word in lyrics if word not in stop_words and word not in string.punctuation])

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

    def get_sentiment(self, df, item, by=None):
        if by == 'abum':
            self.get_album_sentiment(df, item)
        if by == 'song':
            self.get_song_sentiment(df, item)

    def get_album_sentiment(self, df, album):
        # Sentiment gathering
        pos = df[df.Album == album].pos.sum()
        neg = df[df.Album == album].neg.sum()
        neu = df[df.Album == album].neu.sum()
        tot = pos + neg + neu

        self.vals = [pos / tot, neg / tot, neu / tot]

    def get_song_sentiment(self, df, song):
        pos = df[df.Song == song].pos.sum()
        neg = df[df.Song == song].neg.sum()
        neu = df[df.Song == song].neu.sum()
        tot = pos + neg + neu

        self.vals = [pos / tot, neg / tot, neu / tot]

    def get_songs_to_analyze(self, df):
        self.songs_to_analyze = input('Input name of song(s) to analyze, separated by a comma: ').split(',')
        self.songs_to_analyze = [song.strip() for song in self.songs_to_analyze]

    def graph(self, df, how=None, by='song'):
        if by == 'album':
            items_to_graph = self.albums_to_analyze
        elif by == 'song':
            items_to_graph = self.songs_to_analyze
        # Plot albums
        if 'pie' in how:
            for item in items_to_graph:
                self.get_sentiment(df, item, by)
                gr.pieplot(df, item, self.vals)