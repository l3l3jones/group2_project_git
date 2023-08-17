import requests


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
