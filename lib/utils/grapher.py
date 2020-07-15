import matplotlib.pyplot as plt

def pieplot(df, album, save_file=None):
    '''
    Creates a pie chart for the sentiment of the album for the provided DataFrame

    Parameters:
    - df (pd.DataFrame): 
        - a dataframe containing the album to analyze
    - album (string)
        - the title of the album to plot
    - save_file=None (bool)
        - specifies if and where the resulting chart should be saved
    '''
    # Sentiment gathering
    pos = df[df.Album == album].pos.sum()
    neg = df[df.Album == album].neg.sum()
    neu = df[df.Album == album].neu.sum()
    tot = pos + neg + neu
    
    # Plotting & Titling
    plt.pie([pos / tot, neg / tot, neu / tot], autopct='%1.0f%%')
    plt.legend(['Negative', 'Positive', 'Neutral'])
    plt.title('"{}" Sentiment'.format(album))

    # Outputting
    plt.show()
    if save_file is not None:
        plt.savefig(save_file)
        
    plt.close()