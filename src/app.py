from flask import Flask, render_template, request, jsonify
import requests
from utils import (
    get_genres,
    extract_movie_data,
    get_movies_by_keyword,
    get_movies_by_genre,
)
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

#  In a production environment the api key would be stored in a environment variable on the server.

api_key = "eb7191390acbcface8cf637d866e443c"


@app.route("/")
def get_movies():
    # url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}"
    # response = requests.get(url)
    # data = response.json()
    #
    return render_template("movies.html")


@app.route("/search")
def search_movies():
    keyword = request.args.get("keyword")
    genre = request.args.get("genre")
    print(f"Keyword: {keyword}")
    print(f"Genre: {genre}")

    if keyword and genre:

        # still need to get working
        movies = get_movies_by_keyword(keyword)
        filtered_movies = []
        for movie in movies:
            # print(movie["genre_ids"])
            for genre in movie["genre_ids"]:
                # print(type(id))
                # print(type(genre))
                if genre == str(id):
                    # print("yes")
                    filtered_movies.append(movie)

        print(filtered_movies)

    elif keyword:

        return get_movies_by_keyword(keyword)

    elif genre:

        return get_movies_by_genre(genre)


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
