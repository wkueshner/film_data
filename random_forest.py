import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv('movie_info.csv')

# Handling missing values (Example: filling with mode for categorical and median for numerical)
df.fillna({
    'Director 1': df['Director 1'].mode()[0],
    'Director 2': df['Director 2'].mode()[0],
    'Director 3': df['Director 3'].mode()[0],
    'Genre 1': df['Genre 1'].mode()[0],
    'Genre 2': df['Genre 2'].mode()[0],
    'Genre 3': df['Genre 3'].mode()[0],
    'Writer 1': df['Writer 1'].mode()[0],
    'Writer 2': df['Writer 2'].mode()[0],
    'Writer 3': df['Writer 3'].mode()[0],
    'Writer 4': df['Writer 4'].mode()[0],
    'Actor 1': df['Actor 1'].mode()[0],
    'Actor 2': df['Actor 2'].mode()[0],
    'Actor 3': df['Actor 3'].mode()[0],
    'Actor 4': df['Actor 4'].mode()[0],
    'Plot': '',
    'Language': df['Language'].mode()[0],
    'Country': df['Country'].mode()[0],
    'Awards': '',
    'BoxOffice (USD)': df['BoxOffice (USD)'].median()
}, inplace=True)

# Define features and target variable
X = df.drop(['Rotten Tomatoes Rating', 'Title', 'imdbID', 'Plot'], axis=1)
y = df['Rotten Tomatoes Rating']

# Define categorical and numerical features
categorical_features = ['Director 1', 'Director 2', 'Director 3', 'Genre 1', 'Genre 2', 'Genre 3', 
                        'Writer 1', 'Writer 2', 'Writer 3', 'Writer 4', 'Actor 1', 'Actor 2', 
                        'Actor 3', 'Actor 4', 'Rated', 'Released', 'Language', 'Country', 'Awards', 'DVD']
numerical_features = ['Year', 'IMDB Rating', 'Metacritic Rating', 'Runtime', 'imdbVotes', 'BoxOffice (USD)']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Define the model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')
