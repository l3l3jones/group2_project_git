from flask import Flask, request, jsonify, render_template
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


# route that returns the genres and matches id to description; sent to genres dropdown in front end

@app.route('/genres')
def dropdown_genres():
    # creating new instance of Genres class
    genre_instance = Genres()
    # calling the method to get genres from external API
    genres = genre_instance.get_genres()
    # sending the genres to Front End
    return jsonify({"genres": genres})


# route used when no keyword is given; can filter by genre & then by decade if any chosen; does not work with now
# playing
@app.route("/movies/genre")
def discover_movies_by_genre():
    # getting the arguments from the get request
    decade = request.args.get('decade')
    genre = request.args.get('genre')
    # creating new instance of class MoviesByGenre and calling the method
    movies_by_genre = MoviesByGenre()
    data = movies_by_genre.get_movies_by_genre(genre, decade)
    # sending the movies by genre/decade to FE
    return jsonify(data)


# route for now playing movies to load on first accessing the page; brings back 1 page of now playing movies

@app.route("/loading_page")
def get_now_playing_movies():
    # calling the moviedb api for movies playing in UK cinemas, 1 page only for the landing page to have interesting
    # movies
    url = f"https://api.themoviedb.org/3/movie/now_playing"
    params = {"api_key": api_key, "language": "en-GB", "page": 1, "region": "GB"}

    response = requests.get(url, params=params)
    data = response.json()
    # creating new Genres class
    genres_instance = Genres()
    genres = genres_instance.get_genres()
    # appending the names of genre id's to the movie["genre_names"] in case we want to display them on FE
    for movie in data["results"]:
        g = []
        for genre in genres:
            if genre["id"] in movie["genre_ids"]:
                g.append(genre["name"])
        movie["genre_names"] = g
    # transforming the data in a nice movie format
    movie_data = extract_movie_data(data)
    return jsonify(movie_data)


# route used for keyword search that works with filtering by decade or genre
@app.route('/movies/search')
def search_movies_by_decade_genre():
    # getting the arguments query, decade, genre from the FE get request
    query = request.args.get('query')
    decade = request.args.get('decade')
    genre = request.args.get('genre')
    # creating new instance of the class
    movies_by_decade = MoviesByDecadeGenreKeyword()
    # calling the class method to get the movies from moviedb API and process them
    data = movies_by_decade.get_movies_by_decade_genre(query, decade, genre)
    # sending the movie data in JSON format
    return jsonify(data)


# route used when now playing checkbox ticked & there is a keyword ; can filter by decade and genre
@app.route('/movies/now_playing_search')
def search_movies_now_playing_by_decade_genre():
    # getting the arguments query, decade, genre from the FE get request
    query = request.args.get('query')
    decade = request.args.get('decade')
    genre = request.args.get('genre')
    # creating new instance of the class
    movies_now_playing = MoviesByDecadeGenreKeyword()
    # calling the class method to get the movies playing in cinemas from moviedb API and process them
    data = movies_now_playing.get_now_playing_with_search(query, decade, genre)
    # sending the movie data in JSON format
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
