"""Tests for the render module."""
import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

from source import render


class Render(unittest.TestCase):

    @parameterized.expand([
        (
            {"1": {"definition": "a type of stock", "part": "noun"}},
            "noun: a type of stock",
        ),
        (
            {
                "1": {"definition": "definition 1", "part": "part 1"},
                "2": {"definition": "definition 2", "part": "part 2"},
            },
            "<sup>1</sup>part 1: definition 1</br><sup>2</sup>part 2: definition 2",
        ),
    ])
    def test_format_definitions(self, data, expected):
        result = render._format_definitions(data)
        self.assertEqual(result, expected)
