"""Tests for words module."""
import unittest

from wotdb import words


class Words(unittest.TestCase):

    def test_get_random_word(self):
        result = words._get_random_word()
        assert result
