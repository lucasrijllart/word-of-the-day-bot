"""Module handling retrieval of random words and their definitions.

WordsAPI
username: lucas.rijllart@hotmail.com
password: <in lastpass>
https://rapidapi.com/dpventures/api/wordsapi/endpoints
"""
import json

import requests

BASE_API = "https://wordsapiv1.p.rapidapi.com/"

HEADERS = {
    "x-rapidapi-key": "8d02058f51msh5f15d59c4557d70p13503cjsn19946f965c3b",
    "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
    "useQueryString": "true",
}

MAX_TRIES = 10


def get_random_word():
    """Gets random word from API."""
    random_word_endpoint = BASE_API + "words/?random=true"
    response = requests.get(random_word_endpoint, headers=HEADERS)
    data = json.loads(response.text)
    return data["word"]


def get_definitions(word):
    """Gets definition and part of speech description of given word."""
    definition_endpoint = f"{BASE_API}words/{word}/definitions"
    response = requests.get(definition_endpoint, headers=HEADERS)
    data = json.loads(response.text)
    return data["definitions"]


def get_word_and_defintions():
    
    def format_definition(definition):
        return definition["partOfSpeech"] + ": " + definition["definition"]

    word = get_random_word()
    print("Got random word:", word)

    definitions_result = get_definitions(word)
    if definitions_result and len(definitions_result) > 1:
        definitions = ""
        for index, definition in enumerate(definitions_result[:3]):
            print(definition, index)
            formatted = format_definition(definition)
            definitions += f"<sup>{index}</sup>{formatted}<br>"
    elif definitions_result and len(definitions_result) == 1:
        definitions = format_definition(definitions_result[0])
    else:
        definitions = None
    print("Got definitions:", definitions)
    return word, definitions
