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

MAX_DEFINITION_ATTEMPTS = 15

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
    if response.status_code != 200:
        raise Exception(f"WordsAPI request was {response.status_code}: {response.text}")
    assert response.status_code == 200
    logging.info("WordsAPI request successful, status_code=%s" % response.status_code)
    return response.json()


def _parse_random_word_response(response):
    word = response.get("word")

    data = {}
    results = response.get("results", [])
    for index, result in enumerate(results, start=1):
        definition = result.get("definition")
        part = result.get("partOfSpeech")
        if definition and part:
            data[str(index)] = {"definition": definition, "part": part}
    return word, data


def get_word_and_data():
    """Return the random word and its definitions."""
    definitions = None
    attempt = 1
    while not definitions and attempt <= MAX_DEFINITION_ATTEMPTS:
        data = _get_random_word()
        word, definitions = _parse_random_word_response(data)
        logging.info("Word: %s, definitions: %d, attempt: %d"
                     % (word, len(definitions), attempt))
        attempt += 1
    if attempt > MAX_DEFINITION_ATTEMPTS:
        raise Exception("Too many attempts at random words with no definitions.")
    return word, definitions
