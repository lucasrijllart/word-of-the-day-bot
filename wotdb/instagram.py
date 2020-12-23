"""Module handling posting to instagram.
https://github.com/ohld/igbot
https://www.geeksforgeeks.org/post-a-picture-automatically-on-instagram-using-python/
"""
from os import getenv

from instabot import Bot

def post(image_path, caption):
    """Posts an image to instagram."""
    username = getenv("INSTAGRAM_USERNAME")
    password = getenv("INSTAGRAM_PASSWORD")
    if not username or not password:
        raise Exception("Instagram username/password could not be retrieved from env.")
    bot = Bot()
    bot.login(username=username, password=password)
    bot.upload_photo(image_path, caption=caption)
