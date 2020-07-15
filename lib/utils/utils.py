# Note: While for the most part, lyricsgenius has functionality to not include songs with these certain words, these functions were 
# included in order to leave song names that solely consist of one of these phrases

def trim_songs(df, remix=False, unfinished=False):
    '''
    Remove songs from a list depending on user preference. Can remove remix songs or duplicate songs titles. 
    Note that for some artists, the majority of an album can be remixes. While removing them can drastically
    cut down on songs analyzed, keeping them will likely add repetitive results.

    Args:
        df : (DataFrame)
            dataframe containing all songs to consider
        remix=False : (bool)
            specifies whether or not remix songs should be removed
        unfinished=False : (bool)
            specifies whether or not "unfinished" songs should be removed
    '''
    if remix:
        df = remove_remix(df)
    if unfinished:
        df = remove_unfinished(df)
    
    return df

def remove_remix(df):
    remix_words = ['remix', 'alternate', 'cover', 'music video']
    songs_to_remove = [song for song in df.Song.values if any([remix_word in song.lower() \
                        for remix_word in remix_words]) and song.lower() not in remix_words]
    print('songs to remove: ', songs_to_remove)
    df = df.loc[~df.Song.isin(songs_to_remove)]

    return df

def remove_unfinished(df):
    unfinished_words = ['snippet', 'note', 'leak', 'demo']
    songs_to_remove = [song for song in df.Song.values if any([unfinished_word in song.lower() \
                        for unfinished_word in unfinished_words]) and song.lower() not in unfinished_words]
    print('songs to remove: ', songs_to_remove)
    df = df.loc[~df.Song.isin(songs_to_remove)]   
    return df