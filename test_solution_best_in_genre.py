# Tests for solution_best_in_genre.py using Python 3.12.10
import io
import json
import unittest
from unittest.mock import patch

from solution_best_in_genre import bestInGenre


class _FakeResponse:
    """Simple context manager to mimic urllib responses."""

    def __init__(self, payload: dict):
        self._buffer = io.BytesIO(json.dumps(payload).encode("utf-8"))
        self.status = 200

    def read(self) -> bytes:
        return self._buffer.getvalue()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class TestBestInGenre(unittest.TestCase):
    def test_selects_highest_rating_single_page(self):
        page_payload = {
            "page": 1,
            "total_pages": 1,
            "data": [
                {"name": "Show A", "genre": "Drama, Action", "imdb_rating": 8.1},
                {"name": "Show B", "genre": "Action", "imdb_rating": 9.0},
            ],
        }
        with patch("urllib.request.urlopen", return_value=_FakeResponse(page_payload)):
            self.assertEqual(bestInGenre("Action"), "Show B")

    def test_tie_breaks_alphabetically(self):
        page_payload = {
            "page": 1,
            "total_pages": 1,
            "data": [
                {"name": "Zeta Show", "genre": "Comedy", "imdb_rating": 8.5},
                {"name": "Alpha Show", "genre": "Comedy", "imdb_rating": 8.5},
            ],
        }
        with patch("urllib.request.urlopen", return_value=_FakeResponse(page_payload)):
            self.assertEqual(bestInGenre("comedy"), "Alpha Show")

    def test_paginates_and_finds_on_second_page(self):
        first_page = {
            "page": 1,
            "total_pages": 2,
            "data": [
                {"name": "Irrelevant", "genre": "Drama", "imdb_rating": 7.0},
            ],
        }
        second_page = {
            "page": 2,
            "total_pages": 2,
            "data": [
                {"name": "Deep Pick", "genre": "Sci-Fi", "imdb_rating": 9.2},
            ],
        }
        responses = iter([_FakeResponse(first_page), _FakeResponse(second_page)])
        with patch("urllib.request.urlopen", side_effect=lambda *_, **__: next(responses)):
            self.assertEqual(bestInGenre("sci-fi"), "Deep Pick")

    def test_invalid_input_returns_empty_string(self):
        self.assertEqual(bestInGenre(123), "")
        self.assertEqual(bestInGenre(""), "")


if __name__ == "__main__":
    unittest.main()
