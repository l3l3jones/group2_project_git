from flask import Flask, request, jsonify
import requests
from BackEnd.utils import (
    MoviesByGenre,
    MoviesByDecadeGenreKeyword,
    Genres,
    extract_movie_data
)
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# IMPORTANT please enter a valid TMDB API key below, this is only an example key, it will not work
API_KEY = ""please_enter_api_key_here""


# using flask decorator to handle Not Found Errors and return a JSON response
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


# using flask decorator to handle Internal Errors and return a JSON response
@app.errorhandler(500)
def internal_error(e):
    return jsonify(error="Internal server error"), 500


# route that returns the genres and matches id to description; sent to genres dropdown in front end
@app.route('/genres')
def dropdown_genres():
    # creating new instance of Genres class

    genre_instance = Genres()
    # calling the method to get genres from external API

    genres = genre_instance.get_genres()
    # sending the genres to Front End

    return jsonify({"genres": genres})


# route used when no keyword is given; can filter by genre & then by decade if any chosen;
# does not work with now playing
@app.route("/movies/genre")
def discover_movies_by_genre():
    try:
        # getting the args from the get request
        decade = request.args.get('decade')
        genre = request.args.get('genre')

        # creating new instance of class MoviesByGenre and calling the method
        movies_by_genre = MoviesByGenre()
        data = movies_by_genre.get_movies_by_genre(genre, decade)

        # sending the movies by genre/decade to FE
        return jsonify(data)

    # raising exception that catches ValueError for invalid data formats/ type conversion
    except ValueError as e:
        return jsonify(error=str(e)), 400

    # this catches any request-related exceptions
    except requests.RequestException as e:
        return jsonify(error=f"API request error: {e}"), 502


# route for now playing movies to load on first accessing the page; brings back 1 page of now playing movies

@app.route("/loading_page")
def get_now_playing_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing"
    params = {"api_key": API_KEY, "language": "en-GB", "page": 3, "region": "GB"}

    # calling the moviedb api for movies playing in UK cinemas, 1 page only for the landing page
    try:
        response = requests.get(url, params=params)
        data = response.json()

    # handling any request related errors
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to establish a connection to the API: {e}")

    # transforming the data in a nice movie format
    movie_data = extract_movie_data(data)
    return jsonify(movie_data)


# route used for keyword search that works with filtering by decade or genre
@app.route('/movies/search')
def search_movies_by_decade_genre():
    try:
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

    # raising exception that catches ValueError for invalid data formats/ type conversion
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        return jsonify(error=str(e)), 500

    # this catches any request-related exceptions
    except requests.RequestException as e:
        # This catches any request-related exceptions
        return jsonify(error=f"API request error: {e}"), 502


# route used when now playing checkbox ticked & there is a keyword ; can filter by decade and genre
@app.route('/movies/now_playing_search')
def search_movies_now_playing_by_decade_genre():

    try:
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

    # raising exception that catches ValueError for invalid data formats/ type conversion
    except ValueError as e:
        return jsonify(error=str(e)), 400

    # This catches any request-related exceptions
    except requests.RequestException as e:
        return jsonify(error=f"API request error: {e}"), 502


if __name__ == "__main__":
    app.run(debug=True)
