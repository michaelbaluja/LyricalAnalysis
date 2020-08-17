# Lyrical Analysis

LyricalAnalysis is a python library combining aspects of the nltk package and LyricsGenius python-based genius.com api package to allow users to view sentiment breakdown for their favorite artists, albums, and songs.

## Installation

To install LyricalAnalysis, download the zip file from github or clone the reposity.

```bash
git clone https://github.com/michaelbaluja/LyricalAnalysis.git
```

## Setup
A Geniuse API client key is required for use. A client access key can be gathered from https://genius.com/api-clients, but requires a genius account to do so. While the key can be passed in as a runtime argument, or given when prompted if not already provided, the key can also be added as an environment variable GENIUS_KEY. In the case that an api key is passed in as a runtime argument but the environment variable is already set, the runtime provided key will be used, and the environment variable key will be ignored.

## Usage

In order to easily analyze an artist, run *main.py* from the command line with the proper artist/song to analyze, along with any other arguments for analysis (see chart below). 

```bash
python src/main.py --from_cache --artist 'Childish Gambino' --by 'album' --plot 'line'
```
- Note that for artist names that consist of more than one word, the name must be surrounded by a matching set of single or double quotations

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please ensure all suggested code does not cause issues with the current codebase.

## License
[MIT](https://choosealicense.com/licenses/mit/)