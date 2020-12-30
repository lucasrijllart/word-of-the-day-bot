"""Module containing entrypoint definitions."""
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


def post_to_twitter():
    """Generate definition image and post to twitter."""
    main_process_handler("dark_twitter.html", height=512, width=1024, twitter_post=True)
