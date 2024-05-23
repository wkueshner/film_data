import csv
import requests
import logging

# Set up logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

# API details
api_url = "http://www.omdbapi.com/"
api_key = "5c04e3ce"

def convert_rating(rating, source):
    if not rating:  # Check if the rating is empty
        return ""
    if source == "IMDB Rating":
        return f"{float(rating.split('/')[0]) * 10:.0f}"  # Convert X.X/10 to XX
    elif source == "Rotten Tomatoes Rating":
        return rating.rstrip('%')  # Remove % from XX%
    elif source == "Metacritic Rating":
        return f"{int(rating.split('/')[0]):.0f}"  # Convert X-XXX/100 to XX
    return ""

def convert_box_office(box_office):
    if not box_office:
        return ""
    return box_office.replace('$', '').replace(',', '')

def convert_imdb_votes(imdb_votes):
    if not imdb_votes:
        return ""
    return imdb_votes.replace(',', '')

# Open the CSV file containing movie titles
with open('movie_titles_wikipedia.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the first row
    # Prepare to write to a new CSV file
    with open('movie_metadata.csv', mode='w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        # Write headers with new order
        headers = ["Title", "Year", "Genre 1", "Genre 2", "Genre 3", "Director", "IMDB Rating", "Rotten Tomatoes Rating", "Metacritic Rating", "Rated", "Released", "Runtime", "Writer 1", "Writer 2", "Writer 3", "Writer 4", "Actor 1", "Actor 2", "Actor 3", "Actor 4", "Plot", "Language", "Country", "Awards", "Poster", "Metascore", "imdbRating", "imdbVotes", "imdbID", "Type", "DVD", "BoxOffice (USD)", "Production", "Website", "Response"]
        csv_writer.writerow(headers)
        
        # Iterate over each row in the movie_titles.csv
        for index, row in enumerate(csv_reader):
            #if index < 10:  # Limit to the first 100 entries after the first row
            if row:
                title = row[0].strip()
                year = row[1].strip() if len(row) > 1 else None
                # Prepare parameters for API request
                params = {
                    'apikey': api_key,
                    't': title
                }
                if year:  # Only add 'y' parameter if year is not None or empty
                    params['y'] = year
                try:
                    # Make the request to the API
                    response = requests.get(api_url, params=params)
                    if response.status_code != 200:
                        logging.error(f"HTTP Error {response.status_code} for {title} {year}")
                        continue
                    data = response.json()
                    if data['Response'] == 'True':
                        # Extract relevant data and write to the new CSV
                        ratings = {d['Source']: d['Value'] for d in data.get("Ratings", [])}
                        genres = data.get("Genre", "").split(", ")
                        genre1 = genres[0] if len(genres) > 0 else ""
                        genre2 = genres[1] if len(genres) > 1 else ""
                        genre3 = genres[2] if len(genres) > 2 else ""
                        actors = data.get("Actors", "").split(", ")
                        actor1 = actors[0] if len(actors) > 0 else ""
                        actor2 = actors[1] if len(actors) > 1 else ""
                        actor3 = actors[2] if len(actors) > 2 else ""
                        actor4 = actors[3] if len(actors) > 3 else ""
                        writers = data.get("Writer", "").split(", ")
                        writer1 = writers[0] if len(writers) > 0 else ""
                        writer2 = writers[1] if len(writers) > 1 else ""
                        writer3 = writers[2] if len(writers) > 2 else ""
                        writer4 = writers[3] if len(writers) > 3 else ""
                        csv_writer.writerow([
                            data.get("Title", ""),
                            data.get("Year", ""),
                            genre1,
                            genre2,
                            genre3,
                            data.get("Director", ""),
                            convert_rating(ratings.get("Internet Movie Database", ""), "IMDB Rating"),
                            convert_rating(ratings.get("Rotten Tomatoes", ""), "Rotten Tomatoes Rating"),
                            convert_rating(ratings.get("Metacritic", ""), "Metacritic Rating"),
                            data.get("Rated", ""),
                            data.get("Released", ""),
                            data.get("Runtime", ""),
                            writer1,
                            writer2,
                            writer3,
                            writer4,
                            actor1,
                            actor2,
                            actor3,
                            actor4,
                            data.get("Plot", ""),
                            data.get("Language", ""),
                            data.get("Country", ""),
                            data.get("Awards", ""),
                            data.get("Poster", ""),
                            data.get("Metascore", ""),
                            data.get("imdbRating", ""),
                            convert_imdb_votes(data.get("imdbVotes", "")),
                            data.get("imdbID", ""),
                            data.get("Type", ""),
                            data.get("DVD", ""),
                            convert_box_office(data.get("BoxOffice", "")),
                            data.get("Production", ""),
                            data.get("Website", ""),
                            data.get("Response", "")
                        ])
                    else:
                        logging.error(f"No data found for {title} {year}: {data.get('Error', 'Unknown Error')}")
                except Exception as e:
                    # Log any errors with the title and year
                    logging.error(f"Error fetching data for {title} {year}: {str(e)}")
