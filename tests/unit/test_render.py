"""Tests for the render module."""
from datetime import date
import unittest

from parameterized import parameterized

from wotdb import render


class Render(unittest.TestCase):

    def test_format_date(self):
        """Ensure the date is fomatted correctly."""
        test_date = date(year=2020, month=1, day=1)
        result = render._format_date(test_date)
        self.assertEqual(result, "Wednesday 1st of January 2020")

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
