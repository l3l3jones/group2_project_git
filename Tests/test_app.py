import unittest
from unittest.mock import patch

from requests import RequestException

from BackEnd.app import app
from BackEnd.utils import MoviesByGenre, MoviesByDecadeGenreKeyword, Genres, extract_movie_data

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('BackEnd.app.requests.get')
    def test_get_genres(self, mock_get):
        # Mock the response from the API
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"genres": [{"id": 28, "name": "Action"}]}

        # Call the endpoint
        response = self.client.get('/genres')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['genres']), 1)
        self.assertEqual(data['genres'][0]['name'], 'Action')

    @patch('BackEnd.utils.MovieProviders.get_movie_watch_providers')
    @patch('BackEnd.app.requests.get')
    def test_discover_movies_by_genre(self, mock_get, mock_watch_providers):
        # Mock the response from the API
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Movie 1",
                    "genre": "Action",
                    "release_date": "2001-01-01",
                    "rating": 8.5,
                    "director": "John Doe",
                    "id": 724209

                }
            ]
        }

        mock_watch_providers.return_value = {

        }
        # Call the endpoint with query parameters
        response = self.client.get('/movies/genre?genre=28&decade=2000')
        data = response.get_json()
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['title'], 'Movie 1')
        self.assertEqual(data[0]['rating'], 8.5)

    @patch('BackEnd.app.Genres')
    @patch('BackEnd.app.requests.get')
    def test_get_now_playing_movies(self, mock_get, mock_genres):
        # Mock the response from the API
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Movie 1",
                    "genre_ids": [28, 12],
                    "release_date": "2001-01-01",
                    "rating": 8.5,
                    "director": "John Doe",
                    "overview": "Short description of movie",
                    "poster_path": "/vB8o2p4ETnrfiWEgVxHmHWP9yRl.jpg",
                    "vote_average": 6.5,
                    "id": 724209

                }
            ]
        }

        # Mock the Genres class and its method
        mock_genres_instance = mock_genres.return_value
        mock_genres_instance.get_genres.return_value = [
            {"id": 28, "name": "Action"},
            {"id": 12, "name": "Adventure"},
        ]
        # Call the endpoint
        response = self.client.get('/loading_page')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Movie 1')
        self.assertIn('genres', data[0])


# Edge cases

class TestMoviesByGenre(unittest.TestCase):
    @patch.object(MoviesByGenre, 'get_movies_by_genre')
    def test_empty_response(self, mock_get_movies_by_genre):
        mock_get_movies_by_genre.return_value = []
        response = app.test_client().get('/movies/genre?genre=28')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])


# test ensures the system behaves correctly when provided a valid decade but there are no movies from that decade.
class TestMoviesByDecadeGenreKeyword(unittest.TestCase):
    @patch.object(MoviesByDecadeGenreKeyword, 'get_movies_by_decade_genre')
    def test_valid_decade_no_movies(self, mock_method):
        mock_method.return_value = []
        response = app.test_client().get('/movies/search?query=action&decade=1920&genre=28')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)


class TestGenres(unittest.TestCase):
    @patch.object(Genres, 'get_genres')
    def test_empty_response(self, mock_get_genres):
        mock_get_genres.return_value = []
        response = app.test_client().get('/genres')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'genres': []})


class TestExtractMovieData(unittest.TestCase):
    def test_missing_results_key(self):
        data = {"other_key": "value"}
        result = extract_movie_data(data)
        self.assertEqual(result, [])


class TestMoviesByGenreWithAPIUnavailable(unittest.TestCase):

    @patch('BackEnd.utils.requests.get')
    def test_api_unavailable(self, mock_requests_get):
        # Set up the mock to simulate API unavailability
        mock_requests_get.side_effect = RequestException("API is unavailable")

        # Create an instance of MoviesByGenre
        movies_by_genre = MoviesByGenre()

        # Call the method that interacts with the API
        response = movies_by_genre.get_movies_by_genre(genre='action', decade='2010s')

        # Check if the response is as expected when the API is unavailable
        self.assertIn('error', response)
        self.assertEqual(response['error'], "An error occurred: API is unavailable")


if __name__ == '__main__':
    unittest.main()
