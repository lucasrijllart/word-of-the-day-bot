"""Package initialisation. Holds main function."""
import logging
import subprocess

from .render import render_template, create_image
from .words import get_word_and_data

MAX_OVERALL_TRIES = 1


def main_process():
    """Generate image based on random word and definition."""
    word, definitions = get_word_and_data()
    render = render_template(word, definitions)
    image = create_image(render)
    return image


def run():
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
            result = main_process()
        except Exception as e:
            logging.exception(e)
            continue
        finally:
            tries += 1
    logging.info("End of run")
    if result:
        subprocess.run(["xdg-open", result])
