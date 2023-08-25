import requests

# we should hide API key
API_KEY = "eb7191390acbcface8cf637d866e443c"
BASE_URL = "https://api.themoviedb.org/3"


# class that calls external API for all genres returned with id & description
class Genres:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    # class method that calls moviedb genre list api and returns them
    def get_genres(self):

        try:
            url = f"{self.base_url}/genre/movie/list"
            params = {"api_key": self.api_key}
            response = requests.get(url, params=params)

            # raises exception if the response doesn't have the genres key
            try:
                genres = response.json()["genres"]
                return genres
            except KeyError:
                print("Error: 'genres' key not found in the API response.")

        # exception to catch any request-related exceptions
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while trying to connect to the API: {e}")


# class that gets 10 pages of now playing movies, used later when filtering movies that are now playing in cinema
class NowPlaying:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    # Class method that calls the now_playing moviedb endpoint and returns 10 pages of movies
    def get_now_playing(self, pages=10):
        url = f"{self.base_url}/movie/now_playing"

        # list to store movies from all pages
        all_movies = []

        # get request for each of the 10 pages
        for page in range(1, pages + 1):
            params = {"api_key": self.api_key, "region": "GB", "page": page}
            try:
                response = requests.get(url, params=params)
                # appending all the movies to the all_movies list
                all_movies.extend(response.json().get("results", []))
            # error message if fetching fails
            except requests.exceptions.RequestException as e:
                print(f"Error: Unable to establish a connection to the API: {e}")

        return all_movies


# function that extracts data from external API response and reworks it in a usable form
# used in '/landing_page' endpoint
def extract_movie_data(data):
    movies = []
    genders_instance = Genres()
    genres = genders_instance.get_genres()

    for movie in data["results"]:
        try:
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

        # exception raised if no 'results' key in data
        except KeyError as e:
            print(f"Error: Missing key in movie data : {e}")
    return movies


# class used to return movies by genre without a keyword typed in search box;
# if a decade is given it will filter by decade as well

class MoviesByGenre:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    # class method that takes the arguments sent from front end and returns movies by genre / decade
    def get_movies_by_genre(self, genre=None, decade=None, max_pages=3):

        # list to store the movies from all pages
        movies = []

        # looping through the 3 pages and call the moviedb /discover endpoint; this can't be filtered by keyword
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_genres={genre}&page={page}"

            try:
                response = requests.get(url)
                # appending movies from each page to movies list
                movies.extend(response.json()["results"])

            # error message if the get request fails
            except requests.exceptions.RequestException as e:
                print(f"An error occured while trying to fetch movies: {e}")

        # in case a decade is chosen, the movies are filtered by decade;
        # the decade parameter defalts to None if decade not chosen
        if decade:
            try:
                start_year = int(decade)
                end_year = start_year + 9
                movies = [
                    movie
                    for movie in movies
                    if int(movie["release_date"].split("-")[0])
                       in range(start_year, end_year + 1)
                ]

            # raising exception in case the decade is not the expected format
            except ValueError:
                print("Error: Invalid decade parameter.")

        # Instantiate MovieProviders class
        movie_providers = MovieProviders()

        if movies:
            for movie in movies:
                try:
                    # For each movie, get the streaming providers
                    providers = movie_providers.get_movie_watch_providers(movie["id"])

                # exception raised if the movie id is not fond
                except Exception as e:
                    print(f"Error fetching providers for movie {movie['id']}: {e}")

                # if providers are found for the movies, new key 'providers'
                # that has the list of providers as value is added to the movie
                if providers:
                    movie["providers"] = providers

        return movies


# helper function to filter by decade and genre; also filters out movies without a poster path
def valid_movie(movie, start_year, end_year, genres):
    # valid_year & has_genre are set to True as they are optional choices in dropdown list front end
    try:
        valid_year = True
        has_genre = True
        # checks if there is url for the image
        has_poster = movie["poster_path"]

        # in case a decade is chosen, the movies will be filtered by release date
        if start_year and end_year:
            # getting the year from the release date format
            year = int(movie["release_date"].split("-")[0])
            # a valid movie should be between start_year and end_year
            valid_year = start_year <= year <= end_year

        # if a genre is chosen, the movies will be filtered by genre as well
        if genres:
            has_genre = int(genres) in movie["genre_ids"]

        # returning movies that match the requirements
        return valid_year and has_poster and has_genre

    # handling exceptions
    except (TypeError, ValueError, IndexError) as e:
        print("An error occurred: (e)")
        return False


# class for main search by keyword with option to filter by decade and genre
# 2 main methods depending on if the now playing checkbox is ticked or not

class MoviesByDecadeGenreKeyword:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    # method used to get now playing movies by keyword with filtering options
    # parameters decade & genre default to None as they are optional
    def get_now_playing_with_search(self, query, decade=None, genre=None, max_pages=5):

        # list to hold movies from all pages returned
        movies = []

        # api call to search/movie with query word for each of 5 pages
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={query}&page={page}"

            try:
                response = requests.get(url)
                # adding the movies from each page to the movies list
                movies.extend(response.json()["results"])

            # exception to catch any request-related exceptions
            except requests.RequestException as e:
                print(f"Error fetching movies for query '{query}': {e}")

        # creating a new instance of the class NowPlaying and getting 10 pages of movies playing in cinema at the moment
        now_playing = NowPlaying()
        now_playing_movies = now_playing.get_now_playing()

        # creating a list with all the titles in the now_playing_movies
        now_playing_titles = [movie["title"] for movie in now_playing_movies]
        # checking if the titles of movies main list match any titles from the now_playing_titles and filtering out
        # the ones that don't
        filtered_nowplaying_movies = [
            movie for movie in movies if movie["title"] in now_playing_titles
        ]

        # if decade is chosen, processing the start and end year of the decade & matching the format
        if decade:
            try:
                s_year = int(decade)
                e_year = s_year + 9
            except ValueError:
                print(f"Error converting decade '{decade}' to integer")
        else:
            s_year = e_year = None

        # checking that the movie has a poster, filtering the movies if a decade or genre was chosen
        if decade or genre:
            filtered_nowplaying_movies = [
                movie
                for movie in filtered_nowplaying_movies
                if valid_movie(movie, s_year, e_year, genre)
            ]

        # returning the list of movies playing in cinemas that match the criteria
        return filtered_nowplaying_movies

    # this is almost the same apart from filtering for now_playing so returns all the movies with the keyword
    # method used to get movies by query with filtering options
    # parameters decade & genre default to None as they are optional
    def get_movies_by_decade_genre(self, query, decade=None, genre=None, max_pages=5):
        # list to hold movies from all pages returned

        movies = []
        # api call to search/movie with query word for each of 5 pages

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={query}&page={page}"
            try:
                response = requests.get(url)
                # adding the movies from each page to the movies list
                movies.extend(response.json()["results"])

            # exception to catch any request-related exceptions
            except requests.RequestException as e:
                print(f"Error fetching movies for query '{query}': {e}")

        # if decade is chosen, processing the start and end year of the decade & matching the format
        if decade:
            try:
                s_year = int(decade)
                e_year = s_year + 9
            except ValueError as e:
                print(f"Error converting decade '{decade}' to integer")
        # if decade not provided, setting the start& end year to None
        else:
            s_year = e_year = None

        # checking that the movie has a poster, filtering the movies if a decade or genre was chosen
        if decade or genre:
            movies = [
                movie for movie in movies if valid_movie(movie, s_year, e_year, genre)
            ]

        # adding the movie providers list to each movie if applicable
        movie_providers = MovieProviders()

        if movies:
            for movie in movies:
                try:
                    # For each movie, get the streaming providers
                    providers = movie_providers.get_movie_watch_providers(movie["id"])
                # exception raised if the movie id is not found
                except Exception as e:
                    print(f"Error fetching providers for movie {movie['id']}: {e}")

                # if providers are found for the movies, new key 'providers'
                # that has the list of providers as value is added to the movie
                if providers:
                    movie["providers"] = providers
        # returning the list of movies that match the criteria
        return movies


# creating a class for movie providers
class MovieProviders:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    # method that gets the providers from TMDB API for each movie by id
    def get_movie_watch_providers(self, movie_id):

        url = f"{self.base_url}/movie/{movie_id}/watch/providers"
        params = {"api_key": self.api_key}

        try:
            response = requests.get(url, params=params)
            data = response.json()
            # get the providers for GB
            gb_providers = data.get("results", {}).get("GB", {})
            # return "flatrate", which is just streaming (apparently), where the display priority is less than 12
            # These are the more well-know providers
            filtered_providers = [provider for provider in gb_providers.get("flatrate", []) if
                                  provider.get("display_priority", 0) < 12]
            return filtered_providers

        # exception to catch any request-related exceptions
        except requests.exceptions.RequestException as e:
            print(f"Error establishing connection to the API for movie {movie_id}: {e}")
