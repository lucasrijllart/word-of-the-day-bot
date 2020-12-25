"""Package initialisation. Holds main function."""
import logging
import os
import subprocess
import time

from . import data
from .render import create_image_from_template
from .utils import timestamp
from .words import get_word_and_data

MAX_OVERALL_TRIES = 2


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


def _main_process_flow(open_file):
    """Generate image based on random word and definition."""
    data_dir = _make_directory(data.__path__[0])
    word, definitions = get_word_and_data(data_dir)
    image = create_image_from_template(word, definitions, data_dir)
    if open_file:
        subprocess.run(["xdg-open", image])
    return image


def main_process_handler(open_file=False):
    """Handle any exceptions from main process and just retry."""
    logging.basicConfig(
        format="%(asctime)s|%(levelname)s %(module)s: %(message)s",
        level=logging.INFO
    )
    logging.info("Started run")
    result = None
    tries = 1
    while not result and tries <= MAX_OVERALL_TRIES:
        logging.info("Running main process, try %s" % tries)
        try:
            result = _main_process_flow(open_file)
        except Exception as e:
            logging.exception(e)
            time.sleep(1)  # wait after getting exception
            continue
        finally:
            tries += 1
    logging.info("End of run")
