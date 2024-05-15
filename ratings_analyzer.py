import csv

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

# Read the existing movie metadata CSV
with open('movie_metadata.csv', mode='r', encoding='utf-8') as infile:
    csv_reader = csv.DictReader(infile)
    # Prepare to write to a new CSV file
    with open('movie_scores.csv', mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ["Title", "Year", "Genre 1", "Genre 2", "Genre 3", "Director", "IMDB Rating", "Rotten Tomatoes Rating", "Metacritic Rating"]
        csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        
        # Iterate over each row in the movie_metadata.csv
        for row in csv_reader:
            # Convert ratings to a common format
            # Write the first nine columns to the new CSV
            csv_writer.writerow({
                "Title": row["Title"],
                "Year": row["Year"],
                "Genre 1": row["Genre 1"],
                "Genre 2": row["Genre 2"],
                "Genre 3": row["Genre 3"],
                "Director": row["Director"],
                "IMDB Rating": row["IMDB Rating"],
                "Rotten Tomatoes Rating": row["Rotten Tomatoes Rating"],
                "Metacritic Rating": row["Metacritic Rating"]
            })
