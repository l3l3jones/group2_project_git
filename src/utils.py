import requests

# we should hide API key
api_key = "eb7191390acbcface8cf637d866e443c"


# class that calls external API for all genres returned with id & description
class Genres:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    def get_genres(self):
        url = f"{self.base_url}/genre/movie/list"
        params = {"api_key": self.api_key}

        response = requests.get(url, params=params)
        genres = response.json()["genres"]
        return genres


# class that gets 10 pages of now playing movies, used later when filtering movies that are now playing in cinema
class NowPlaying:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    def get_now_playing(self, pages=10):
        url = f"{self.base_url}/movie/now_playing"
        base_url = "https://api.themoviedb.org/3/movie/now_playing"
        all_movies = []

        for page in range(1, pages + 1):
            params = {
                'api_key': self.api_key,
                'region': 'GB',
                'page': page
            }

            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                all_movies.extend(response.json().get('results', []))
            else:
                print(f"Error {response.status_code}: Failed to fetch now playing movies for the UK on page {page}.")

        return all_movies


# function that extracts data from external API response and reworks it in a usable form
def extract_movie_data(data):
    movies = []
    genders_instance = Genres()
    genres = genders_instance.get_genres()

    for movie in data["results"]:
        movies.append(
            {
                "title": movie["title"],
                "overview": movie["overview"],
                "poster_path": movie["poster_path"],
                "release_date": movie["release_date"],
                "vote_average": movie["vote_average"],
                "genres": [
                    genre["name"]
                    for genre in genres
                    if genre["id"] in movie["genre_ids"]
                ],
            }
        )

    return movies


# class MoviesByKeyword:
#     def __init__(self):
#         self.api_key = "eb7191390acbcface8cf637d866e443c"
#         self.base_url = "https://api.themoviedb.org/3"
#
#     def get_movies_by_keyword(self, keyword):
#         url = f"{self.base_url}/search/keyword?api_key={self.api_key}&query={keyword}"
#         response = requests.get(url)
#         data = response.json()
#         keyword_id = data["results"][0]["id"]
#
#         url_search = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_keywords={keyword_id}"
#         response = requests.get(url_search)
#         movies = response.json()["results"]
#
#         return movies


# class used to return movies by genre without a keyword typed in search box; if a decade is given
# it will filter by decade as well

class MoviesByGenre:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    def get_movies_by_genre(self, genre=None, decade=None, max_pages=5):

        movies = []
        # looping through the 5 pages
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_genres={genre}&page={page}"
            response = requests.get(url)

            if response.status_code == 200:
                movies.extend(response.json()['results'])

            if response.status_code != 200:
                print(f"Error {response.status_code}: Failed to fetch movies.")

        if decade:
            start_year = int(decade)
            end_year = start_year + 9
            movies = [movie for movie in movies if
                          int(movie['release_date'].split("-")[0]) in range(start_year, end_year + 1)]

        return movies


# class for main search by keyword with option to filter by decade and genre
# 2 main methods depending if now playing checkbox is ticked
# quite long so should probably be split up in more manageable bits, but didn't have time

class MoviesByDecadeGenreKeyword:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    # method used to get now playing movies by keyword with filtering options
    def get_now_playing_with_search(self, query, decade=None, genre=None, max_pages=5):

        all_movies = []

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={query}&page={page}"
            response = requests.get(url)

            if response.status_code == 200:
                all_movies.extend(response.json()['results'])
        # checking if the title of the movie is in now_playing
        now_playing = NowPlaying()
        now_playing_movies = now_playing.get_now_playing()
        now_playing_titles = [movie['title'] for movie in now_playing_movies]
        print(now_playing_movies)
        filtered_nowplaying_movies = [movie for movie in all_movies if movie['title'] in now_playing_titles]
        print(filtered_nowplaying_movies)
        # filtering by decade if one is given and matching the format
        if decade:
            decade = int(decade)
            s_year = int(f"{decade}-01-01".split("-")[0])
            e_year = s_year + 9
        else:
            s_year = e_year = None

        # checking that the movie has a poster; has_genre & has_poster set to True as they are optional

        def valid_movie(movie, start_year, end_year, genres):
            try:
                is_valid_year = True
                has_genre = True
                has_poster = movie['poster_path']

                if start_year and end_year:
                    year = int(movie['release_date'].split("-")[0])
                    is_valid_year = start_year <= year <= end_year

                if genres:
                    has_genre = int(genres) in movie['genre_ids']

                return is_valid_year and has_poster and has_genre

            except (TypeError, ValueError, IndexError):
                return False

        if decade or genre:
            filtered_nowplaying_movies = [movie for movie in filtered_nowplaying_movies if
                                          valid_movie(movie, s_year, e_year, genre)]

        return filtered_nowplaying_movies

    # this is exactly the same apart from filtering for now_playing so returns all the movies with the keyword
    def get_movies_by_decade_genre(self, query, decade=None, genre=None, max_pages=5):
        all_movies = []

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={query}&page={page}"
            response = requests.get(url)

            if response.status_code == 200:
                all_movies.extend(response.json()['results'])

        if decade:
            decade = int(decade)
            s_year = int(f"{decade}-01-01".split("-")[0])
            e_year = s_year + 9
        else:
            s_year = e_year = None

        def valid_movie(movie, start_year, end_year, genres):
            try:
                is_valid_year = True
                has_genre = True
                has_poster = movie['poster_path']

                if start_year and end_year:
                    year = int(movie['release_date'].split("-")[0])
                    is_valid_year = start_year <= year <= end_year

                if genres:
                    has_genre = int(genres) in movie['genre_ids']

                return is_valid_year and has_poster and has_genre

            except (TypeError, ValueError, IndexError):
                return False

        if decade or genre:
            all_movies = [movie for movie in all_movies if valid_movie(movie, s_year, e_year, genre)]

        return all_movies
