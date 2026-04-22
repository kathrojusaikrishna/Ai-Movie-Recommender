import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("../backend/data/tmdb_5000_movies.csv")
credits = pd.read_csv("../backend/data/tmdb_5000_credits.csv")

movies = movies.merge(credits, on='title')
movies = movies[['title', 'overview', 'genres', 'keywords', 'cast']]
movies.dropna(inplace=True)

def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def fetch_cast(text):
    return [i['name'] for i in ast.literal_eval(text)[:3]]

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(fetch_cast)

movies['tags'] = movies['overview'] + " " + \
    movies['genres'].apply(lambda x: " ".join(x)) + " " + \
    movies['keywords'].apply(lambda x: " ".join(x)) + " " + \
    movies['cast'].apply(lambda x: " ".join(x))

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)

# Save files
pickle.dump(movies, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))