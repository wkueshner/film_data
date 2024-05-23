import pandas as pd
import matplotlib.pyplot as plt

# Load the movie metadata CSV file
df = pd.read_csv('movie_metadata.csv')

# Convert relevant columns to numeric, forcing errors to NaN
df['IMDB Rating'] = pd.to_numeric(df['IMDB Rating'], errors='coerce')
df['Rotten Tomatoes Rating'] = pd.to_numeric(df['Rotten Tomatoes Rating'], errors='coerce')
df['Metacritic Rating'] = pd.to_numeric(df['Metacritic Rating'], errors='coerce')

# Convert the 'Year' column to numeric, forcing errors to NaN
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Filter the DataFrame to include only the last 30 years
current_year = pd.Timestamp.now().year
df = df[df['Year'] >= (current_year - 30)]

# Group by year and calculate the mean for each rating
average_ratings_per_year = df.groupby('Year').agg({
    'IMDB Rating': 'mean',
    'Rotten Tomatoes Rating': 'mean',
    'Metacritic Rating': 'mean'
}).reset_index()

# Sort the DataFrame by Year
average_ratings_per_year = average_ratings_per_year.sort_values(by='Year')

# Plot the average ratings per year
plt.figure(figsize=(10, 6))
plt.plot(average_ratings_per_year['Year'], average_ratings_per_year['IMDB Rating'], label='IMDB Rating', marker='o')
plt.plot(average_ratings_per_year['Year'], average_ratings_per_year['Rotten Tomatoes Rating'], label='Rotten Tomatoes Rating', marker='o')
plt.plot(average_ratings_per_year['Year'], average_ratings_per_year['Metacritic Rating'], label='Metacritic Rating', marker='o')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Average Rating')
plt.title('Average Movie Ratings Per Year (Last 30 Years)')
plt.legend()
plt.grid(True)

# Set x-axis ticks to be every 5 years for better readability
plt.xticks(ticks=average_ratings_per_year['Year'][::5], rotation=45)

# Show the plot
plt.show()
