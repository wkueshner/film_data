import pandas as pd
import matplotlib.pyplot as plt

# Load the movie metadata CSV file
df = pd.read_csv('movie_metadata.csv')

# Convert relevant columns to numeric, forcing errors to NaN
df['Rotten Tomatoes Rating'] = pd.to_numeric(df['Rotten Tomatoes Rating'], errors='coerce')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Filter the DataFrame to include only the last 30 years
current_year = pd.Timestamp.now().year
df = df[df['Year'] >= (current_year - 30)]

# Group by year and Genre 1, then calculate the mean Rotten Tomatoes Rating
average_ratings_per_year_genre = df.groupby(['Year', 'Genre 1']).agg({
    'Rotten Tomatoes Rating': 'mean'
}).reset_index()

# Pivot the DataFrame to have genres as columns
average_ratings_pivot = average_ratings_per_year_genre.pivot(index='Year', columns='Genre 1', values='Rotten Tomatoes Rating')

# Plot the average Rotten Tomatoes Ratings per year per genre
plt.figure(figsize=(12, 8))
for genre in average_ratings_pivot.columns:
    plt.plot(average_ratings_pivot.index, average_ratings_pivot[genre], label=genre, marker='o')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Average Rotten Tomatoes Rating')
plt.title('Average Rotten Tomatoes Ratings Per Year Per Genre (Last 30 Years)')
plt.legend(title='Genre 1', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Set x-axis ticks to be every 5 years for better readability
plt.xticks(ticks=average_ratings_pivot.index[::5], rotation=45)

# Show the plot
plt.tight_layout()
plt.show()
