# Lyrical Analysis

LyricalAnalysis is a python library combining aspects of the nltk package and LyricsGenius python-based genius.com api package to allow users to view sentiment breakdown for their favorite artists, albums, and songs.

## Installation

To install LyricalAnalysis, download the zip file from github or clone the reposity.

```bash
git clone https://github.com/michaelbaluja/LyricalAnalysis.git
```

## Usage

In order to easily analyze an artist, run *main.py* from the command line with the proper artist to analyze and genius client access key. A client access key can be gathered from https://genius.com/api-clients, but requires a genius account to do so. 

```bash
python src/main.py --key genius-client-access-key-here --artist 'Childish Gambino'
```
- Note that for artist names that consist of more than one word, the name must be surrounded by a matching set of single or double quotations

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please ensure all suggested code does not cause issues with the current codebase.

## License
[MIT](https://choosealicense.com/licenses/mit/)