from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

import requests

def fetch_poster(movie_title):
    api_key = os.getenv("TMDB_API_KEY")

    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
        response = requests.get(url,verify=False)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None

    except Exception as e:
        print("Error fetching poster:", e)
        return None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = similarity[index]

        movie_list = sorted(list(enumerate(distances)),
                            reverse=True,
                            key=lambda x: x[1])[1:6]

        results = []

        for i in movie_list:
            title = movies.iloc[i[0]].title
            poster = fetch_poster(title)

            results.append({
                "title": title,
                "poster": poster
            })

        return results

    except:
        return [{"title": "Movie not found", "poster": None}]
    
@app.route('/')
def home():
    return "API is running!"

@app.route('/recommend', methods=['GET'])
def recommend_api():
    movie = request.args.get('movie')
    result = recommend(movie)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)