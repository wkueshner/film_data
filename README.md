This is a simple repository containing scripts that can:

-[fetch every movie with its own page on wikipedia](wikipedia_films_scraper.py)
- [pass these movies' titles (and release years, in case they're a remake or share the same name) into the open movie database (OMDB) API and parse the response data into a pandas dataframe](movie_metadata_fetcher.py)
- [analyze the data](ratings_analyzer.py) to:
-- identify historical trends in IMBD, Tomatometer, and Metacritic ratings

## Requirements

- Python 3.10 or later
- pandas
- requests

## Usage

```bash
python movie_metadata_fetcher.py
```

