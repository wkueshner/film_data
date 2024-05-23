import pandas as pd

# Load the CSV file into a DataFrame with low_memory=False to avoid DtypeWarning
df = pd.read_csv('movie_metadata.csv', low_memory=False)

# Split "Director" into "Director 1", "Director 2", and "Director 3"
directors_split = df['Director'].str.split(',', expand=True)
df['Director 1'] = directors_split[0]
df['Director 2'] = directors_split[1]
df['Director 3'] = directors_split[2]

# Delete the specified columns
columns_to_delete = ['Poster', 'Metascore', 'imdbRating', 'Production', 'Website', 'Response', 'Type']
df.drop(columns=columns_to_delete, inplace=True)

# Strip " min" from runtime entries
df['Runtime'] = df['Runtime'].str.replace(' min', '')

# Replace DVD entry with True/False
df['DVD'] = df['DVD'].apply(lambda x: False if x == 'N/A' else True)

# Reorder columns to ensure "Director 1", "Director 2", and "Director 3" are next to each other
columns_order = ['Director 1', 'Director 2', 'Director 3'] + [col for col in df.columns if col not in ['Director 1', 'Director 2', 'Director 3']]
df = df[columns_order]

# Save the modified DataFrame to a new CSV file
df.to_csv('movie_info.csv', index=False)
