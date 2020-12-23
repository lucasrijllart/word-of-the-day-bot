"""Tests for words module."""
import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

from source import words


class Words(unittest.TestCase):

    def test_headers(self):
        """Ensure the function returns a filled out dict."""
        result = words._headers()
        for key, value in result.items():
            assert key
            assert value

    @unittest.mock.patch("source.words.requests")
    def test_get_random_word(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        response = {"word": "pro-danish"}
        mock_response.json.return_value = response
        mock_requests.get.return_value = mock_response
        result = words._get_random_word()
        self.assertEqual(result, response)

    @parameterized.expand([
        (
            {
                "word": "pro-danish",
                "rhymes": {"all": "-eɪnɪʃ"},
                "pronunciation": {},
            },
            "pro-danish",
            {}
        ),
        (
            {
                "word": "tape record",
                "results": [{
                    "definition": "record with a tape recorder",
                    "partOfSpeech": "verb",
                    "inCategory": ["recording", "transcription"],
                    "typeOf": ["record", "tape"],
                    "derivation": ["tape recorder", "tape recording"]
                }]
            },
            "tape record",
            {"1": {"definition": "record with a tape recorder", "part": "verb"}}
        ),
        (
            {
                "word": "kidney",
                "results": [
                    {"definition": "a thing", "partOfSpeech": "noun"},
                    {"definition": "another thing", "partOfSpeech": "verb"}
                ]
            },
            "kidney",
            {
                "1": {"definition": "a thing", "part": "noun"},
                "2": {"definition": "another thing", "part": "verb"},
            }
        ),
    ])
    def test_parse_random_word_response(self, response, expected_word, expected_data):
        """Ensure the function parses a response from WordAPI and extracts the correct
        data.
        """
        word, data = words._parse_random_word_response(response)
        self.assertEqual(word, expected_word)
        self.assertEqual(data, expected_data)

    @unittest.mock.patch("source.words.requests")
    def test_get_word_and_data(self, mock_requests):
        """Ensure the function gets a random word and data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "word": "subjugator",
            "results": [{
                "definition": "a conqueror who defeats and enslaves",
                "partOfSpeech": "noun",
                "typeOf": ["conqueror", "vanquisher"],
                "derivation": ["subjugate"]
            }],
            "syllables": {"count": 4, "list": ["sub", "ju", "ga", "tor"]}
        }
        mock_requests.get.return_value = mock_response
        expected_data = {
            "1": {"definition": "a conqueror who defeats and enslaves", "part": "noun"}
        }
        word, data = words.get_word_and_data()
        self.assertEqual(word, "subjugator")
        self.assertEqual(data, expected_data)
