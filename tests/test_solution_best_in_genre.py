# Tests for solution_best_in_genre.py using Python 3.12.10
import io
import json
import os
import sys
import unittest
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(ROOT, "challenges"))

from solution_best_in_genre import bestInGenre


def _configure_run_mode() -> str:
    """
    Determine run mode based on CLI flags.

    Supported flags:
        --all   -> run mock + live
        --live  -> run only live tests
        --mock  -> run only mock tests (default)
    """
    flag_map = {
        "--all": "all",
        "--live": "live",
        "--mock": "mock",
    }
    for arg in list(sys.argv[1:]):
        if arg in flag_map:
            sys.argv.remove(arg)
            return flag_map[arg]
    return "mock"


RUN_MODE = _configure_run_mode()


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
                {"name": "Zeta", "genre": "Comedy", "imdb_rating": 8.5},
                {"name": "Alpha", "genre": "Comedy", "imdb_rating": 8.5},
            ],
        }
        with patch("urllib.request.urlopen", return_value=_FakeResponse(page_payload)):
            self.assertEqual(bestInGenre("comedy"), "Alpha")

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
        with patch(
            "urllib.request.urlopen", side_effect=lambda *_, **__: next(responses)
        ):
            self.assertEqual(bestInGenre("sci-fi"), "Deep Pick")

    def test_invalid_input_returns_empty_string(self):
        self.assertEqual(bestInGenre(123), "")
        self.assertEqual(bestInGenre(""), "")


class TestBestInGenreLive(unittest.TestCase):
    def test_action_genre_live(self):
        # Uses the real API; expected value based on published sample data.
        self.assertEqual(bestInGenre("Action"), "Game of Thrones")

    def test_comedy_genre_live(self):
        # A secondary live check; still relies on stable API data.
        result = bestInGenre("Comedy")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")


def load_tests(loader, tests, pattern):
    """Select test suites based on RUN_MODE."""
    suite = unittest.TestSuite()
    if RUN_MODE in ("mock", "all"):
        suite.addTests(loader.loadTestsFromTestCase(TestBestInGenre))
    if RUN_MODE in ("live", "all"):
        suite.addTests(loader.loadTestsFromTestCase(TestBestInGenreLive))
    return suite


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
