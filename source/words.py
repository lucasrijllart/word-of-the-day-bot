"""Module handling retrieval of random words and their definitions.

WordsAPI
username: lucas.rijllart@hotmail.com
password: <in lastpass>
https://rapidapi.com/dpventures/api/wordsapi/endpoints
"""
import logging
import os

import requests

from dotenv import load_dotenv
load_dotenv()

BASE_API = "https://wordsapiv1.p.rapidapi.com/"


def _headers(key_env_var="X_RAPIDAPI_KEY"):
    """Constuct headers for WordsAPI request."""
    key = os.getenv(key_env_var)
    return {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "useQueryString": "true",
    }


def _get_random_word():
    """Gets random word from API."""
    random_word_endpoint = BASE_API + "words/?random=true"
    response = requests.get(random_word_endpoint, headers=_headers())
    assert response.status_code == 200
    logging.info("WordsAPI request successful, status_code=%s" % response.status_code)
    return response.json()


def _parse_random_word_response(response):
    word = response.get("word")
    print("word:", word)
    data = {}
    results = response.get("results", [])
    for index, result in enumerate(results, start=1):
        definition = result.get("definition")
        part = result.get("partOfSpeech")
        data[str(index)] = {"definition": definition, "part": part}
    print("data:", data)
    return word, data


def get_word_and_data():
    """Return the random word and its definitions."""
    data = _get_random_word()
    word, data = _parse_random_word_response(data)
    return word, data
