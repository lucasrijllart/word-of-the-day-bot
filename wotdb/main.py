"""Package initialisation. Holds main function."""
import logging
import os
import subprocess
import time

from dotenv import load_dotenv

from . import data
from .facebook import Facebook
from .render import render_template, create_image
from .twitter import Twitter
from .utils import timestamp
from .words import get_word_and_data

MAX_OVERALL_TRIES = 5


def _make_directory(path):
    """Create directory to store run files."""
    directory = os.path.join(path, timestamp())
    try:
        os.mkdir(directory)
    except OSError:
        raise Exception("Creation of the directory %s failed." % directory)
    else:
        logging.info("Successfully created directory %s" % directory)
    return directory


def post_twitter(data_dir, word, image_path):
    twitter_bot = Twitter(data_dir)
    twitter_bot.tweet_image(f"{word} #WordOfTheDay", image_path)


def post_facebook(data_dir, word, image_path):
    max_attempts = 10
    attempt = 1
    post_id = None
    while not post_id and attempt <= max_attempts:
        logging.info("Attempting Facebook post, attempt %s" % attempt)
        try:
            facebook_bot = Facebook(data_dir)
            facebook_bot.authenticate()
            post_id = facebook_bot.publish_post(word, image_path)
        except Exception as e:
            logging.exception(e)
            logging.info("Waiting %ss" % (2 ** attempt))
            time.sleep(2 ** attempt)  # exponential backoff
            continue
        finally:
            attempt += 1
    return post_id


def _retrieve_word_and_definition(data_dir, template, width, height):
    """Generate image based on random word and definition."""
    word, definitions = get_word_and_data(data_dir)
    render_path = render_template(word, definitions, data_dir, template)
    image_path = create_image(render_path, data_dir, width, height)
    return word, image_path


def main_process_handler(
        template="template_1.html",
        height=1000,
        width=1000,
        open_file=False,
        twitter_post=False,
        facebook_post=False,
):
    """Handle any exceptions from main process and just retry."""
    logging.basicConfig(
        format="%(asctime)s|%(levelname)s %(module)s: %(message)s",
        level=logging.INFO
    )
    logging.info("Started run")
    load_dotenv(verbose=True)

    data_dir = _make_directory(data.__path__[0])
    word, image_path = _retrieve_word_and_definition(data_dir, template, width, height)
    
    if open_file:
        subprocess.run(["xdg-open", image_path])
    if twitter_post:
        post_twitter(data_dir, word, image_path)
    if facebook_post:
        post_facebook(word, image_path)
    logging.info("End of run")
