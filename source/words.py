"""Module handling retrieval of random words and their definitions.

WordsAPI
username: lucas.rijllart@hotmail.com
password: <in lastpass>
https://rapidapi.com/dpventures/api/wordsapi/endpoints
"""
import json
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
    data = json.loads(response.text)
    return data["word"]


def _get_definitions(word):
    """Gets definition and part of speech description of given word."""
    definition_endpoint = f"{BASE_API}words/{word}/definitions"
    response = requests.get(definition_endpoint, headers=_headers())
    data = json.loads(response.text)
    return data["definitions"]


def _format_definition(definition):
    """Format definition with part of speech before the definition."""
    return definition["partOfSpeech"] + ": " + definition["definition"]


def get_word_and_definitions():
    """Return the random word and its definitions."""
    word = _get_random_word()
    print("Got random word:", word)

    definitions_result = _get_definitions(word)
    if definitions_result and len(definitions_result) > 1:
        definitions = ""
        for index, definition in enumerate(definitions_result[:3]):
            print(definition, index)
            formatted = _format_definition(definition)
            definitions += f"<sup>{index}</sup>{formatted}<br>"
    elif definitions_result and len(definitions_result) == 1:
        definitions = _format_definition(definitions_result[0])
    else:
        definitions = None
    print("Got definitions:", definitions)
    return word, definitions
