import requests

api_key = "eb7191390acbcface8cf637d866e443c"


def get_genres():
    url = f"https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": "eb7191390acbcface8cf637d866e443c"}

    response = requests.get(url, params=params)
    genres = response.json()["genres"]
    return genres


def extract_movie_data(data):
    movies = []
    genres = get_genres()

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


def get_movies_by_keyword(keyword):
    url = (
        f"https://api.themoviedb.org/3/search/keyword?api_key={api_key}&query={keyword}"
    )

    response = requests.get(url)
    data = response.json()

    keyword_id = data["results"][0]["id"]

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_keywords={keyword_id}"

    response = requests.get(url)
    movies = response.json()["results"]

    return movies


def get_movies_by_genre(genre):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre}"

    response = requests.get(url)
    data = response.json()["results"]

    # movie_data = extract_movie_data(data)

    return data
