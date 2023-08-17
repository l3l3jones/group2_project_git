import requests

api_key = "eb7191390acbcface8cf637d866e443c"
# Test cases for genre

# Test searching comedy movies
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?with_genres=35&api_key={api_key}"
)
comedies = response.json()["results"]

assert len(comedies) > 0  # results returned
assert comedies[0]["genre_ids"][0] == 35  # validate genre

# Test searching drama movies
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?with_genres=18&api_key={api_key}"
)
dramas = response.json()["results"]

assert len(dramas) > 0
assert dramas[0]["genre_ids"][0] == 18

# Test filtering by multiple genres
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?with_genres=35,18&api_key={api_key}"
)
movies = response.json()["results"]

assert len(movies) > 0
assert movies[0]["genre_ids"][0] in [35, 18]

# Test invalid genre ID
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?with_genres=999&api_key={api_key}"
)
assert response.status_code == 404


####-------------------------#####

# Test cases for release year

# Test movies released in 2019
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?primary_release_year=2019&api_key={api_key}"
)
movies = response.json()["results"]

assert len(movies) > 0
assert movies[0]["release_date"][:4] == "2019"

# Test movies released in 1980
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?primary_release_year=1980&api_key={api_key}"
)
movies = response.json()["results"]

assert len(movies) > 0
assert movies[0]["release_date"][:4] == "1980"

# Test invalid release year
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?primary_release_year=9999&api_key={api_key}"
)
assert response.status_code == 404

# Test release year range
response = requests.get(
    f"https://api.themoviedb.org/3/discover/movie?primary_release_date.gte=1990&primary_release_date.lte=2000&api_key={api_key}"
)
movies = response.json()["results"]

assert len(movies) > 0
assert "1990" <= movies[0]["release_date"][:4] <= "2000"
