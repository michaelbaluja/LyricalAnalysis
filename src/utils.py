# Note: While for the most part, lyricsgenius has functionality to not include songs with these certain words, these functions were 
# included in order to leave song names that solely consist of one of these phrases

def trim_songs(songs, remix=False, unfinished=False):
    '''
    Remove songs from a list depending on user preference. Can remove remix songs or duplicate songs titles. 
    Note that for some artists, the majority of an album can be remixes. While removing them can drastically
    cut down on songs analyzed, keeping them will likely add repetitive results.

    Args:
        songs : (list)
            list of song names 
        remix=False : (bool)
            specifies whether or not remix songs should be removed
        unfinished=False : (bool)
            specifies whether or not "unfinished" songs should be removed
    '''
    if remix:
        songs = remove_remix(songs)
    if unfinished:
        songs = remove_unfinished(songs)
    
    return songs

def remove_remix(songs):
    remix_words = ['remix', 'alternate', 'cover', 'music video']
    for song in songs:
        # Sees if song contains remix keyword but makes sure the keyword isn't just the name of the song
        if any(remix_word in song.lower() for remix_word in remix_words) and song.lower() not in remix_words:
            songs.remove(song)

    return songs

def remove_unfinished(songs):
    unfinished_words = ['snippet', 'note', 'leak', 'demo']
    for song in songs:
        # Sees if song contains 'unfinishsed' keyword but makes sure the keyword isn't just the name of the song
        if any(unfinished_word in song.lower() for unfinished_word in unfinished_words) and song.lower() not in unfinished_words:
            songs.remove(song)

    return songs 