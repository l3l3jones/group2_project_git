from flask import Flask, request, jsonify
import requests
from utils import (
    MoviesByGenre,
    MoviesByDecadeGenreKeyword,
    # MoviesByKeyword,
    Genres,
    extract_movie_data
)
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

#  We should put api_key in dev environment variable so not everyone has access

api_key = "eb7191390acbcface8cf637d866e443c"

#route that returns the genres and matches id to description; sent to genres dropdown in front end

@app.route('/genres')
def dropdown_genres():
    genre_instance = Genres()
    genres = genre_instance.get_genres()
    return jsonify({"genres": genres})


# @app.route("/")
# def get_movies():
#     url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}"
#     response = requests.get(url)
#     data = response.json()
#     # return render_template("movies.html")
#     return jsonify(data)

# route used when no keyword is given; can filter by genre & then by decade if any chosen; does not work with now playing
@app.route("/movies/genre")
def discover_movies_by_genre():
    decade = request.args.get('decade')
    genre = request.args.get('genre')
    print(decade)
    print(genre)
    movies_by_genre = MoviesByGenre()
    data = movies_by_genre.get_movies_by_genre(genre, decade)

    return jsonify(data)


# @app.route("/search")
# def search_movies():
#     keyword = request.args.get("keyword")
#     genre = request.args.get("genre")
#     print(f"Keyword: {keyword}")
#     print(f"Genre: {genre}")
#
#     if keyword and genre:
#
#         # still need to get working
#         movies = MoviesByKeyword.get_movies_by_keyword(keyword)
#         filtered_movies = []
#         for movie in movies:
#             # print(movie["genre_ids"])
#             for genre in movie["genre_ids"]:
#                 # print(type(id))
#                 # print(type(genre))
#                 if genre == str(id):
#                     # print("yes")
#                     filtered_movies.append(movie)
#
#         print(filtered_movies)
#
#     elif keyword:
#
#         return MoviesByKeyword.get_movies_by_keyword(keyword)
#
#     elif genre:
#
#         return MoviesByGenre.get_movies_by_genre(genre)

#route for now playing movies to load on first accessing the page; brings back 1 page of now playing movies

@app.route("/loading_page")
def get_now_playing_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing"
    params = {"api_key": api_key, "language": "en-GB", "page": 1, "region": "GB"}

    response = requests.get(url, params=params)
    data = response.json()

    genres_instance = Genres()
    genres = genres_instance.get_genres()

    for movie in data["results"]:
        g = []
        for genre in genres:
            if genre["id"] in movie["genre_ids"]:
                g.append(genre["name"])
        movie["genre_names"] = g

    movie_data = extract_movie_data(data)
    return jsonify(movie_data)

# @app.route("/movies/<int:year>")
# def get_movies_by_release_year(year):
#     url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_year={year}"
#
#     response = requests.get(url)
#     data = response.json()
#
#     movie_data = extract_movie_data(data)
#
#     return render_template("movies.html", movies=movie_data)

# route used for keyword search that works with filtering by decade or genre
@app.route('/movies/search')
def search_movies_by_decade_genre():
    query = request.args.get('query')
    decade = request.args.get('decade')
    genre = request.args.get('genre')
    print(genre)
    movies_by_decade = MoviesByDecadeGenreKeyword()
    data = movies_by_decade.get_movies_by_decade_genre(query, decade, genre)
    return jsonify(data)

# route used when now playing checkbox ticked & there is a keyword ; can filter by decade and genre
@app.route('/movies/now_playing_search')
def search_movies_now_playing_by_decade_genre():
    query = request.args.get('query')
    decade = request.args.get('decade')
    genre = request.args.get('genre')
    print(genre)
    movies_now_playing = MoviesByDecadeGenreKeyword()
    data = movies_now_playing.get_now_playing_with_search(query, decade, genre)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
