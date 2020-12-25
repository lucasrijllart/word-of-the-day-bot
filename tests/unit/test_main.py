"""Unit tests for main module."""
import os
import unittest

from wotdb import main


class Main(unittest.TestCase):

    def test_make_directory(self):
        """Ensure function creates a new directory, then remove it."""
        path = os.path.dirname(os.path.abspath(__file__))
        new_directory = main._make_directory(path)
        self.assertTrue(os.path.isdir(new_directory))
        os.rmdir(new_directory)
