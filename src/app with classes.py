from flask import Flask, render_template, request
from utils import get_genres, extract_movie_data

app = Flask(__name__)

api_key = "eb7191390acbcface8cf637d866e443c"

class MovieFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_movies(self):
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {"api_key": self.api_key}

        response = requests.get(url, params=params)
        data = response.json()

        return data["results"]

@app.route("/")
def get_movies_route():
    movie_fetcher = MovieFetcher(api_key)  # Instantiate the MovieFetcher class
    movies = movie_fetcher.get_movies()  # Call the get_movies method
    return render_template("movies.html", movies=movies)

@app.route("/search")
class MovieSearcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = f"https://api.themoviedb.org/3/search/keyword?api_key={api_key}&query={keyword}"


    def search_movies(self, keyword):
        response = requests.get(self.base.url)
        data = response.json()

        keyword_id = data['results'][0]['id']

        url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_keywords={keyword_id}"

        response = requests.get(url)
        movies = response.json()['results']

        return movies


keyword = request.args.get('keyword')  ## may need to be changed based on how the input is structured
movie_searcher = MovieSearcher()
movies = movie_searcher.search_movies(keyword)

@app.route("/movies/genre/<string:genre>")
class GenreFetcher:
    def __init__(self, api_key, genre):
        self.genre = genre
        self.api_key = api_key

    def get_movies_genre(self):
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            movie_data = self.extract_movie_data(data)
            return movie_data
        except requests.exceptions.RequestException as html_error:
            return None

    def extract_movie_data(self, data):
        genre = data.get('genre')
        return genre

genre = 13 #whatever input its going to be
genre_fetcher = GenreFetcher(genre)
movies = genre_fetcher.get_movies_genre()

if movies is None:
    print('An error occured whilst fetching the HTML genre data.')
else:
    pass

@app.route("/now_playing")
class NowPlaying:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_now_playing_movies(self):
        url = "https://api.themoviedb.org/3/movie/now_playing"
        params = {"api_key": self.api_key,
                  "language": "en-GB",
                  "page": 1,
                  "region": "GB"}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            genres = self.get_genres()

            for movie in data["results"]:
                g = []
                for genre in genres:
                    if genre["id"] in movie["genre_ids"]:
                        g.append(genre["name"])
                movie["genre_names"] = g

            return data
        except requests.exceptions.RequestException as html_error:
            return None



api_key = "eb7191390acbcface8cf637d866e443c"
now_playing = NowPlaying(api_key)
now_playing_movies = now_playing.get_now_playing_movies()

if now_playing_movies is None:
    print('An error occured whilst fetching the HTML movie data.')
else:
    pass


@app.route("/movies/<int:year>")
class MovieByReleaseYearFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_movies_by_release_year(self, year):
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {"api_key": self.api_key,
                  "primary_release_year": year}

        response = requests.get(url, params=params)
        data = response.json()

        movie_data = extract_movie_data(data)
        return movie_data


api_key = "eb7191390acbcface8cf637d866e443c"
movie_fetcher = MovieByReleaseYearFetcher(api_key)
year = 2023 ### this would change depending on input, just did this for example
movies = movie_fetcher.get_movies_by_release_year(year)

if __name__ == "__main__":
    app.run(debug=True)

