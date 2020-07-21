import pandas as pd
import numpy as np
import lib.utils.utils as utils # For sanitation 

# For graphing
import lib.utils.grapher as gr

from nltk.tokenize import word_tokenize

class Analyzer():
    def __init__(self, genius, args):
        '''
        Parameters:
        - genius: (lyricsgenius.api)
            - callable api wrapper to make requests to genius.com
        - args: (argparse.ArgumentParser)
            - list of run-time arguments to set analysis parameters
        '''
        self.genius = genius
        self.remove_remix = args.remove_remix
        self.remove_unfinished = args.remove_unfinished

    def analyze_artist(self, artist_to_search, stop_words, sentiment_analyzer, by='album'):
        '''
        Performs sentiment analysis for the provided artist based on the analysis method provided. An artist can be analyzed as a whole, both album, or by song.

        Parameters:
        - artist_to_search: (str)
            - string name for the artist to search for songs from
        - stop_words: (list)
            - list of words to be removed from the lyrics as they don't provide sentiment information
        - sentiment_analyzer: (nltk.SentimentIntensityAnalyzer)
            - analyzer class to provide sentiment information for the words (lyrics) passed in
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
            self.get_songs_to_analyze()

        return df

    def analyze_song(self, song_to_search, stop_words, sentiment_analyzer, song_artist=None):
        '''
        Performs sentiment analysis for the provided song.

        Parameters:
        - song_to_analyze: (str)
            - title of song to analyze
        - stop_words: (set)
            - list of words to be removed from the lyrics as they don't provide sentiment information
        - sentiment_analyzer: (nltk.SentimentIntensityAnalyzer)
            - analyzer class to provide sentiment information for the words (lyrics) passed in
        - song_artist=None: (str)
            - artist of song to search
        '''
        # Create variables to store song info in format easy to work with
        df = pd.DataFrame(columns=['Song', 'Lyrics'])

        while True:
            try:
                song = [self.genius.search_song(song_to_search, artist=song_artist if song_artist is not None else '')]
                # Create dataframe with all necessary song info
                df = df.append({'Song':song_to_search, 'Lyrics':song[0].lyrics}, ignore_index=True)
            except AttributeError:
                song_to_search = input('Please enter correct song to search: ')
            break

        df = self.tokenize(df, stop_words)
        df = self.add_sentiment(df, sentiment_analyzer)
        self.songs_to_analyze = df.Song.values

        return df

    def tokenize(self, df, stop_words):
        '''
        Takes DataFrame containing lists of lyrics, removes all provided stop_words, and separates the lyrics by word

        Parameters:
        - df: (pd.DataFrame)
            - DataFrame containing lyrics to tokenize
        - stop_words: (set)
            - set of all stop_words to remove from our lyrics

        Return:
        - df: (pd.DataFrame)
            - DataFrame with lyrics separated by word
        '''
        # Tokenize lyrics & remove stop words
        df['Lyrics'] = df['Lyrics'].apply(word_tokenize)
        df['Lyrics'] = df['Lyrics'].apply(lambda lyrics: [word for word in lyrics if word not in stop_words])

        return df

    def add_sentiment(self, df, sentiment_analyzer):
        '''
        Provided a DataFrame of lyrics, adds sentiment information given by the provided sentiment analyzer

        Parameters:
        - df: (pd.DataFrame)
            - DataFrame containing lyrics that are parsed by word
        - sentiment_analyzer: (nltk.SentimentIntensityAnalyzer)
            - sentiment analyzer to add provide sentiment information for the provided lyrics
        
        Return:
        - df: (pd.DataFrame)
            - Initial DataFrame with columns for the total number of words per entry, as well as compund, positive (pos), negative (neg), and neutral (neu) sentiment information
        '''
        # Add num_words for each song in order to normalize sentiment
        df['num_words'] = df['Lyrics'].apply(len)
        df['compound'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['compound'] for word in lyrics])) / df['num_words']
        df['pos'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['pos'] for word in lyrics])) / df['num_words']
        df['neu'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['neu'] for word in lyrics])) / df['num_words']
        df['neg'] = df['Lyrics'].apply(lambda lyrics: sum([sentiment_analyzer.polarity_scores(word)['neg'] for word in lyrics])) / df['num_words']

        return df
    
    def get_albums_to_analyze(self, df):
        '''
        Gets user input for the albums to analyze from a list of albums
        
        Parameters:
        - df: (pd.DataFrame)
            - DataFrame of song info to grab album titles from
        '''
        # Get user input for which albums to analyze
        albums = sorted(set(df.Album.values))
        for index, album in enumerate(albums):
            print('{}: {}'.format(index, album))
        self.albums_to_analyze = input('Input number for each album to analyze, separated by a comma: ').split(',')
        self.albums_to_analyze = [albums[int(i)] for i in self.albums_to_analyze]

    def get_songs_to_analyze(self):
        '''
        Gets user input for which songs to analyze from all songs presented 
        '''
        self.songs_to_analyze = input('Input name of song(s) to analyze, separated by a comma: ').split(',')
        self.songs_to_analyze = [song.strip() for song in self.songs_to_analyze]

    def get_sentiment(self, df, item, by=None):
        '''
        Calls the appropriate sentiment object based on how sentiment should be gotten

        Parameters:
        - df: (pd.DataFrame)
            - DataFrame of song information to pass to sentiment getter
        - item: (str)
            - item to collect sentiment for
        - by=None: (str)
            - specifies how to collect sentiment
        '''
        try:
            if by == 'album':
                self.get_album_sentiment(df, item)
            elif by == 'song':
                self.get_song_sentiment(df, item)
            else:
                raise TypeError()
        except TypeError:
            print("An incorrect sentiment scope was passed in. Recieved '{}' but expected 'album' or 'song'".format(by))

    def get_album_sentiment(self, df, album):
        '''
        Gathers sentiment for the album provided

        Parameters:
        - df: (pd.DataFrame)
            - DataFrame of song information to add sentiment to
        - album: (str)
            - album name to add sentiment for
        '''
        # Sentiment gathering
        pos = df[df.Album == album].pos.sum()
        neg = df[df.Album == album].neg.sum()
        neu = df[df.Album == album].neu.sum()
        tot = pos + neg + neu

        self.vals = [pos / tot, neg / tot, neu / tot]

    def get_song_sentiment(self, df, song):
        '''
        Gathers sentiment for the song provided

        Parameters:
        - df: (pd.DataFrame)
            - DataFrame of song information to add sentiment to
        - song: (str)
            - song name to add sentiment for
        '''
        pos = df[df.Song == song].pos.sum()
        neg = df[df.Song == song].neg.sum()
        neu = df[df.Song == song].neu.sum()
        tot = pos + neg + neu

        self.vals = [pos / tot, neg / tot, neu / tot]

    def graph(self, df, how=None, by='song'):
        '''
        Calls appropriate grapher functions

        Parameters:
        - df: (pd.DataFrame)
            - DataFrame of song info to pass to grapher functions
        - how=None: (str)
            - specifies which graphing functions to call
        - by='song': (str)
            - specifies which sentiment info to pass to the grapher functions. default to song since its the smallest unit and can be applicable to all levels
        '''
        if by == 'album':
            items_to_graph = self.albums_to_analyze
        elif by == 'song':
            items_to_graph = self.songs_to_analyze
        # Plot albums
        if 'pie' in how:
            for item in items_to_graph:
                self.get_sentiment(df, item, by)
                gr.pieplot(item, self.vals)
        if 'line' in how:
            sentiment_vals = []
            for item in items_to_graph:
                self.get_sentiment(df, item, by)
                sentiment_vals.append(self.vals)
            gr.lineplot(items_to_graph, sentiment_vals, by)