import matplotlib.pyplot as plt

def pieplot(df, item, vals, save_file=None):
    '''
    Creates a pie chart for the sentiment of the album for the provided DataFrame

    Parameters:
    - df (pd.DataFrame): 
        - a dataframe containing the album to analyze
    - item (str):
        - the title of the item being plotted
    - vals (list)
        - the sentiment values to plot
    - save_file=None (bool)
        - specifies if and where the resulting chart should be saved
    '''
    # Plotting & Titling
    plt.pie(vals, autopct='%1.0f%%')
    plt.legend(['Positive', 'Negative', 'Neutral'])
    plt.title('"{}" Sentiment'.format(item))

    # Outputting
    plt.show()
    if save_file is not None:
        plt.savefig(save_file)
    plt.close()