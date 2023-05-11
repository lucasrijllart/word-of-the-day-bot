"""The entrypoints below are the externally available functions which are used to run
the project. These are run by GitHub Actions and listed in the setup.py.
"""
from . import data
from .main import main_process_handler


def show_data_folder():
    """Return the path to the data folder."""
    print(data.__package__.replace(".", "/"))


def generate_image():
    """Generate definition image only. Used by GitHub actions to save file."""
    main_process_handler("dark_twitter.html")


def generate_and_open():
    """Generate definition image and open file with xdg-open for local use."""
    main_process_handler("dark_twitter.html", open_file=True)


def twitter_post():
    """Generate definition image and post to twitter."""
    main_process_handler("dark_twitter.html", width=1024, height=512, twitter_post=True)


def facebook_post():
    main_process_handler("dark_twitter.html", width=1080, height=1080, facebook_post=True)