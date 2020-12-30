"""Package initialisation. Holds main function."""
import logging
import os
import subprocess
import time

from dotenv import load_dotenv

from . import data
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


def _main_process_flow(template, height, width, open_file, twitter_post):
    """Generate image based on random word and definition."""
    data_dir = _make_directory(data.__path__[0])
    word, definitions = get_word_and_data(data_dir)
    render_path = render_template(word, definitions, data_dir, template)
    image_path = create_image(render_path, data_dir, height, width)
    if open_file:
        subprocess.run(["xdg-open", image_path])
    if twitter_post:
        twitter_bot = Twitter(data_dir)
        twitter_bot.tweet_image(f"{word} #WordOfTheDay", image_path)
    return image_path


def main_process_handler(
        template="template_1.html",
        height=1000,
        width=1000,
        open_file=False,
        twitter_post=False
):
    """Handle any exceptions from main process and just retry."""
    logging.basicConfig(
        format="%(asctime)s|%(levelname)s %(module)s: %(message)s",
        level=logging.INFO
    )
    logging.info("Started run")
    load_dotenv(verbose=True)

    result = None
    tries = 1
    while not result and tries <= MAX_OVERALL_TRIES:
        logging.info("Running main process, try %s" % tries)
        try:
            result = _main_process_flow(template, height, width, open_file, twitter_post)
        except Exception as e:
            logging.exception(e)
            time.sleep(1)  # wait after getting exception
            continue
        finally:
            tries += 1
    logging.info("End of run")
