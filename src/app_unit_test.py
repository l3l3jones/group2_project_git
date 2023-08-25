import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.requests.get')
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

    @patch('app.requests.get')
    def test_discover_movies_by_genre(self, mock_get):
        # Mock the response from the API
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"results": [{"title": "Movie 1"}]}

        # Call the endpoint with query parameters
        response = self.client.get('/movies/genre?genre=28&decade=2000')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Movie 1')

    @patch('app.requests.get')
    def test_get_now_playing_movies(self, mock_get):
        # Mock the response from the API
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"results": [{"title": "Movie 1"}]}

        # Call the endpoint
        response = self.client.get('/loading_page')
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Movie 1')


if __name__ == '__main__':
    unittest.main()


# Edge cases

import unittest
from unittest.mock import patch
from app import app, MoviesByGenre, MoviesByDecadeGenreKeyword, Genres, extract_movie_data

class TestMoviesByGenre(unittest.TestCase):
    @patch.object(MoviesByGenre, 'get_movies_by_genre')
    def test_empty_response(self, mock_get_movies_by_genre):
        mock_get_movies_by_genre.return_value = []
        response = app.test_client().get('/movies/genre?genre=28')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'data': []})


class TestMoviesByDecadeGenreKeyword(unittest.TestCase):
    @patch.object(MoviesByDecadeGenreKeyword, 'get_movies_by_decade_genre')
    def test_invalid_decade(self, mock_get_movies_by_decade_genre):
        mock_get_movies_by_decade_genre.return_value = []
        response = app.test_client().get('/movies/search?query=action&decade=abcd')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)


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

    @patch('your_module_name.requests.get')
    def test_api_unavailable(self, mock_requests_get):
        # Set up the mock to simulate API unavailability
        mock_requests_get.side_effect = Exception("API is unavailable")

        # Create an instance of MoviesByGenre
        movies_by_genre = MoviesByGenre()

        # Call the method that interacts with the API
        response = movies_by_genre.get_movies_by_genre(genre='action', decade='2010s')

        # Check if the response is as expected when the API is unavailable
        self.assertEqual(response, {'error': 'API is unavailable'})



if __name__ == '__main__':
    unittest.main()
