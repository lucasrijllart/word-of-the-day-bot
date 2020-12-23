"""Package initialisation. Holds main function."""
import logging
import subprocess

from render import render_template, create_image
from words import get_word_and_data

MAX_OVERALL_TRIES = 1
MAX_DEFINITION_TRIES = 15


def main_process():
    """Run the whole process post a new word to instagram."""
    word, definitions = get_word_and_data()
    if not definitions:
        tries = 1
        while not definitions and tries <= MAX_DEFINITION_TRIES:
            print("getting")
            word, definitions = get_word_and_data()
            tries += 1
        if tries > MAX_DEFINITION_TRIES:
            raise Exception("Too many attempts to define words with empty results.")

    render = render_template(word, definitions)
    image = create_image(render)
    return image


def run():
    """Handle any exceptions from main process and just retry."""
    logging.basicConfig(
        format="%(asctime)s|%(levelname)s %(module): %(message)s",
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
    return result


if __name__ == "__main__":
    file = run()
    subprocess.run(["xdg-open", file])
