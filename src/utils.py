import requests

api_key = "eb7191390acbcface8cf637d866e443c"


class Genres:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    def get_genres(self):
        url = f"{self.base_url}/genre/movie/list"
        params = {"api_key": self.api_key}

        response = requests.get(url, params=params)
        genres = response.json()["genres"]
        print(genres)
        return genres


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


class MoviesByKeyword:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    def get_movies_by_keyword(self, keyword):
        url = f"{self.base_url}/search/keyword?api_key={self.api_key}&query={keyword}"
        response = requests.get(url)
        data = response.json()
        keyword_id = data["results"][0]["id"]

        url_search = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_keywords={keyword_id}"
        response = requests.get(url_search)
        movies = response.json()["results"]

        return movies


class MoviesByGenre:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    def get_movies_by_genre(self, genre):
        url = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_genres={genre}"
        response = requests.get(url)
        movies = response.json()["results"]

        return movies

        # movie_data = extract_movie_data(data)

        # return data


class MoviesByDecadeGenre:
    def __init__(self):
        self.api_key = "eb7191390acbcface8cf637d866e443c"
        self.base_url = "https://api.themoviedb.org/3"

    def get_now_playing_with_search(self, query, decade, genre=None, max_pages=5):

        all_movies = []

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={query}&page={page}"
            response = requests.get(url)

            if response.status_code == 200:
                all_movies.extend(response.json()['results'])

        now_playing = NowPlaying()
        now_playing_movies = now_playing.get_now_playing()
        now_playing_titles = [movie['title'] for movie in now_playing_movies]
        print(now_playing_movies)
        filtered_movies = [movie for movie in all_movies if movie['title'] in now_playing_titles]
        print(filtered_movies)
        s_year = int(f"{decade}-01-01".split("-")[0])
        e_year = s_year + 9

        def valid_movie(movie, start_year, end_year, genres):
            try:
                year = int(movie['release_date'].split("-")[0])
                has_poster = movie['poster_path']
                has_genre = True

                if genres:
                    has_genre = int(genres) in movie['genre_ids']

                return s_year <= year <= e_year and has_poster and has_genre
            except (TypeError, ValueError, IndexError):
                return False

        filtered_now_playing_movies = [movie for movie in filtered_movies if valid_movie(movie, s_year, e_year, genre)]
        return filtered_now_playing_movies

    def get_movies_by_decade_genre(self, query, decade, genre=None, max_pages=5):
        all_movies = []

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={query}&page={page}"
            response = requests.get(url)

            if response.status_code == 200:
                all_movies.extend(response.json()['results'])

        s_year = int(f"{decade}-01-01".split("-")[0])
        e_year = s_year + 9

        def valid_movie(movie, start_year, end_year, genres):
            try:
                year = int(movie['release_date'].split("-")[0])
                has_poster = movie['poster_path']
                has_genre = True

                if genres:
                    has_genre = int(genres) in movie['genre_ids']

                return s_year <= year <= e_year and has_poster and has_genre
            except (TypeError, ValueError, IndexError):
                return False

        filtered_movies = [movie for movie in all_movies if valid_movie(movie, s_year, e_year, genre)]
        return filtered_movies
