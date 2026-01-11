# Python 3.12.10
"""
Finds the highest-rated TV series in a given genre via the Hackerrank mock API.

Design choices:
    - Standard library only (urllib, json) per constraints.
    - Iterates pages until the reported total_pages, accumulating the best candidate
    by highest imdb_rating, breaking ties with alphabetical order of the name.
    - Genre matching is case-insensitive and splits the comma-separated genre field,
    trimming whitespace to handle multi-genre entries.
    - Returns an empty string on invalid input, missing data, or request/parse errors,
    as a defensive fallback without changing the required signature.
"""
import json
import urllib.request
from typing import List


def bestInGenre(genre: str) -> str:
    """
    Finds the highest-rated TV series in the given genre.

    Parameters:
        genre (str): The genre to search for (e.g., 'Action', 'Comedy', 'Drama')

    Returns:
        str: The name of the highest-rated show in the genre. If there is a tie, returns the alphabetically lower name. Returns the name as a string.

    Notes:
        -    Ties are broken by alphabetical order of the show name
        -    Genre matching is case-insensitive
        -    Shows can have multiple genres (comma-separated)
    """
    if not isinstance(genre, str):
        return ""
    target_genre = genre.strip().lower()
    if not target_genre:
        return ""

    base_url = "https://jsonmock.hackerrank.com/api/tvseries?page="
    page = 1
    total_pages = None
    best_name = ""
    best_rating = float("-inf")

    while True:
        try:
            with urllib.request.urlopen(f"{base_url}{page}") as response:
                raw_payload = response.read()
        except Exception:
            return ""

        try:
            payload = json.loads(raw_payload.decode("utf-8"))
        except Exception:
            return ""

        if total_pages is None:
            total_pages = payload.get("total_pages", 0)

        shows: List[dict] = payload.get("data", [])
        for show in shows:
            genres_value = show.get("genre")
            if not isinstance(genres_value, str):
                continue
            genres = [entry.strip().lower() for entry in genres_value.split(",")]
            if target_genre not in genres:
                continue

            name = show.get("name")
            rating_value = show.get("imdb_rating")
            if not isinstance(name, str):
                continue
            try:
                rating = float(rating_value)
            except (TypeError, ValueError):
                continue

            if rating > best_rating or (
                rating == best_rating and (best_name == "" or name < best_name)
            ):
                best_rating = rating
                best_name = name

        page += 1
        if total_pages is not None and page > total_pages:
            break

    return best_name
