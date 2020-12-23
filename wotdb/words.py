"""Module handling retrieval of random words and their definitions.

WordsAPI
username: lucas.rijllart@hotmail.com
password: <in lastpass>
https://rapidapi.com/dpventures/api/wordsapi/endpoints
"""
import logging
import os
import time

from dotenv import load_dotenv
import requests

WORDAPI_BASE = "https://wordsapiv1.p.rapidapi.com/"

MAX_DEFINITION_ATTEMPTS = 15

RAPIDAPI_KEY_VAR = "X_RAPIDAPI_KEY"

def _headers():
    """Constuct headers for WordsAPI request."""
    load_dotenv(verbose=True)
    key = os.environ.get(RAPIDAPI_KEY_VAR)
    if not key:
        raise Exception(f"Env var '{RAPIDAPI_KEY_VAR}' has value {key}.")
    return {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "useQueryString": "true",
    }


def _get_random_word():
    """Gets random word from API."""
    random_word_endpoint = WORDAPI_BASE + "words/?random=true"
    headers = _headers()
    response = requests.get(random_word_endpoint, headers=headers)
    if response.status_code != 200:
        api_key = headers["x-rapidapi-key"]
        api_key = api_key[-4:] if api_key else api_key
        raise Exception(
            f"WordsAPI request was {response.status_code}: {response.text}. "
            f"Key used: ...{api_key}"
        )
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
        time.sleep(2)  # avoids overwhelming WordsAPI
    if attempt > MAX_DEFINITION_ATTEMPTS:
        raise Exception("Too many attempts at random words with no definitions.")
    return word, definitions
