import unittest
from unittest.mock import Mock, MagicMock, patch
from utils import Genres, NowPlaying, valid_movie, MoviesByDecadeGenreKeyword  # Import classes from the utils module


# 1. Unit tests for get_genres function
class TestGetGenres(unittest.TestCase):

    @patch('utils.requests.get')
    def test_successful_request(self, mock_get):
        # Mock the requests.get function to return a successful response
        mock_response = Mock()
        mock_response.json.return_value = {"genres": [{"id": 1, "name": "Action"}]}
        mock_get.return_value = mock_response

        genres_instance = Genres()  # Create an instance of the Genres class
        genres = genres_instance.get_genres()  # Call the function

        self.assertEqual(len(genres), 1)
        self.assertEqual(genres[0]['name'], "Action")

    @patch('utils.requests.get')
    def test_missing_genres_key(self, mock_get):
        # Mock the requests.get function to return a response without 'genres' key
        mock_response = Mock()
        mock_response.json.return_value = {"other_key": "value"}
        mock_get.return_value = mock_response

        genres_instance = Genres()
        genres = genres_instance.get_genres()
        self.assertIsNone(genres)

    @patch('utils.requests.get', side_effect=Exception('Test error'))
    def test_request_exception(self, mock_get):
        # Mock the requests.get function to raise an exception
        genres_instance = Genres()
        with self.assertRaises(Exception):
            genres_instance.get_genres()


# 2. Unit tests for get_now_playing function
class TestNowPlaying(unittest.TestCase):

    @patch('utils.requests.get')
    def test_get_now_playing(self, mock_get):
        # Create a mock response with sample movie data
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {"title": "Movie 1"},
                {"title": "Movie 2"}
            ]
        }
        mock_get.return_value = mock_response

        now_playing = NowPlaying()

        # Call the function and get the result
        result = now_playing.get_now_playing(pages=1)

        # Assert that the mock get method was called with the correct URL
        mock_get.assert_called_once_with(
            f"{now_playing.base_url}/movie/now_playing",
            params={"api_key": now_playing.api_key, "region": "GB", "page": 1}
        )

        # Assert that the returned result matches the sample movie data
        self.assertEqual(result, [
            {"title": "Movie 1"},
            {"title": "Movie 2"}
        ])


# 3. Unit tests for valid_movie function
class TestValidMovie(unittest.TestCase):

    def test_valid_movie_with_valid_criteria(self):
        movie = {
            "poster_path": "/example_poster.jpg",
            "release_date": "2022-05-15",
            "genre_ids": [28, 12, 16]
        }
        start_year = 2020
        end_year = 2025
        genre = 12

        result = valid_movie(movie, start_year, end_year, genre)
        self.assertTrue(result)

    def test_valid_movie_with_invalid_year(self):
        movie = {
            "poster_path": "/example_poster.jpg",
            "release_date": "2018-09-20",
            "genre_ids": [28, 12, 16]
        }
        start_year = 2020
        end_year = 2025
        genre = 12

        result = valid_movie(movie, start_year, end_year, genre)
        self.assertFalse(result)

    def test_valid_movie_with_invalid_genre(self):
        movie = {
            "poster_path": "/example_poster.jpg",
            "release_date": "2022-03-10",
            "genre_ids": [28, 16]
        }
        start_year = 2020
        end_year = 2025
        genre = 12

        result = valid_movie(movie, start_year, end_year, genre)
        self.assertFalse(result)

    def test_valid_movie_without_poster(self):
        movie = {
            "release_date": "2022-08-30",
            "genre_ids": [12, 16]
        }
        start_year = 2020
        end_year = 2025
        genre = 12

        # Since "poster_path" key is missing, accessing it should raise a KeyError
        with self.assertRaises(KeyError):
            valid_movie(movie, start_year, end_year, genre)


# 4. Unit tests for MoviesByDecadeGenreKeyword class functions
class TestMoviesByDecadeGenreKeyword(unittest.TestCase):

    @patch('utils.requests.get')
    def test_get_now_playing_with_search(self, mock_get):
        # Prepare mock response with multiple pages of results
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"title": f"Movie {i + 1}"} for i in range(20)  # Simulate 20 movies over 4 pages
            ]
        }
        mock_get.return_value = mock_response

        # Create an instance of the class
        movies_instance = MoviesByDecadeGenreKeyword()

        # Test with basic query and max_pages=5
        result = movies_instance.get_now_playing_with_search("action", max_pages=5)

        # Expected length based on the modified mock response
        self.assertEqual(len(result), 100)

# EDGE CASES TESTS for the MoviesByDecadeGenreKeyword Class
# 1. Tests the behaviour when the API returns no movies


class TestNoMoviesReturnedByAPI(unittest.TestCase):

    @patch('utils.requests.get')
    def test_no_movies_returned(self, mock_get):
        # Prepare mock response with no movies
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}  # Empty list of movies
        mock_get.return_value = mock_response

        # Create an instance of the class
        movies_instance = MoviesByDecadeGenreKeyword()

        # Test with a query that should return no movies
        result = movies_instance.get_now_playing_with_search("nonexistent_query")

        self.assertEqual(len(result), 0)

# 2. Test for Edge Case: Invalid keyword search

    @patch('utils.requests.get')
    def test_invalid_keyword(self, mock_get):
        # Prepare mock response with no movies
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        # Create an instance of the class
        movies_instance = MoviesByDecadeGenreKeyword()

        # Test with invalid keyword
        result = movies_instance.get_now_playing_with_search("invalid_keyword")

        # No movies should be returned for an invalid keyword
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
