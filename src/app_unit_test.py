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
