import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TMDB API configuration
API_KEY = "1b7ef21bc179401cb69fb1c8305b56f6"
BASE_URL = "https://api.themoviedb.org/"


def get_movie_data(movie_id):
    endpoint = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,keywords"
    response = requests.get(endpoint)
    return response.json()


def get_popular_movies(page=1):
    endpoint = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
    response = requests.get(endpoint)
    return response.json()['results']


def create_movie_dataframe(movies):
    data = []
    for movie in movies:
        movie_data = get_movie_data(movie['id'])
        genres = ", ".join([genre['name'] for genre in movie_data['genres']])
        cast = ", ".join([actor['name'] for actor in movie_data['credits']['cast'][:3]])
        keywords = ", ".join([keyword['name'] for keyword in movie_data['keywords']['keywords']])

        data.append({
            'id': movie['id'],
            'title': movie['title'],
            'genres': genres,
            'cast': cast,
            'keywords': keywords,
            'overview': movie['overview']
        })
    return pd.DataFrame(data)


def combine_features(row):
    return f"{row['genres']} {row['cast']} {row['keywords']} {row['overview']}"


def get_recommendations(movie_title, cosine_sim, df):
    idx = df[df['title'] == movie_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices]


# Fetch popular movies
popular_movies = get_popular_movies(1)

# Create dataframe
df = create_movie_dataframe(popular_movies)

# Combine features
df['combined_features'] = df.apply(combine_features, axis=1)

# Create count matrix
count = CountVectorizer().fit_transform(df['combined_features'])

# Compute cosine similarity
cosine_sim = cosine_similarity(count)

# Get recommendations
movie_title = "Inception"  # Replace with any movie title from your dataset
recommendations = get_recommendations(movie_title, cosine_sim, df)

print(f"Recommendations for {movie_title}:")
for i, recommendation in enumerate(recommendations, 1):
    print(f"{i}. {recommendation}")