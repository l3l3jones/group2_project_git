from flask import Flask, render_template, request, jsonify
import requests
from utils import get_genres, extract_movie_data

app = Flask(__name__)

#  In a production environment the api key would be stored in a environment variable on the server.

api_key = "eb7191390acbcface8cf637d866e443c"


@app.route("/")
def get_movies():
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}"
    response = requests.get(url)
    data = response.json()

    return render_template("movies.html", movies=data["results"])


@app.route("/search")
def search_movies():
    keyword = request.args.get("keyword")

    url = (
        f"https://api.themoviedb.org/3/search/keyword?api_key={api_key}&query={keyword}"
    )

    response = requests.get(url)
    data = response.json()

    keyword_id = data["results"][0]["id"]

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_keywords={keyword_id}"

    response = requests.get(url)
    movies = response.json()["results"]

    return render_template("movies.html", movies=movies)


@app.route("/movies/genre/<string:genre>")
def get_movies_by_genre(genre):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre}"

    response = requests.get(url)
    data = response.json()

    movie_data = extract_movie_data(data)

    return render_template("movies.html", movies=movie_data)


@app.route("/now_playing")
def get_now_playing_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing"
    params = {"api_key": api_key, "language": "en-GB", "page": 1, "region": "GB"}

    response = requests.get(url, params=params)
    data = response.json()

    genres = get_genres()

    for movie in data["results"]:
        g = []
        for genre in genres:
            if genre["id"] in movie["genre_ids"]:
                g.append(genre["name"])
        movie["genre_names"] = g

    return data


@app.route("/movies/<int:year>")
def get_movies_by_release_year(year):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_year={year}"

    response = requests.get(url)
    data = response.json()

    movie_data = extract_movie_data(data)

    return render_template("movies.html", movies=movie_data)


if __name__ == "__main__":
    app.run(debug=True)
