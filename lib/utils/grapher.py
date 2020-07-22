import matplotlib.pyplot as plt
import numpy as np

def pieplot(item, vals, save_file=None):
    '''
    Creates a pie chart for the sentiment of the item provided

    Parameters:
    - item: (str)
        - the title of the item being plotted
    - vals: (list)
        - the sentiment values to plot
    - save_file=None: (bool)
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

def lineplot(items, vals, by, save_file=None):
    '''
    Creates a line graph for the change in sentiment of the items given

    Parameters:
    - item: (str)
        - the title of the items being plotted
    - vals: (list)
        - the sentiment values to plot
    - save_file=None: (bool)
        - specifies if and where the resulting chart should be saved
    '''
    # Plotting & Titling
    for idx in range(3):
        plt.plot([val[idx] for val in vals], linewidth=2.0)
    plt.title('Sentiment across {}s'.format(by))
    plt.legend(['Positive', 'Negative', 'Neutral'])

    # Axes
    plt.xticks(ticks=np.arange(0, len(items), 1), labels=items)
    plt.yticks(np.arange(0.0, 1.1, 0.1))    

    # Outputting
    plt.show()
    if save_file is not None:
        plt.savefig(save_file)
    plt.close()