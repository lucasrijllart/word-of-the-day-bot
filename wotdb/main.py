"""Package initialisation. Holds main function."""
import logging
import subprocess
import time

from .instagram import post_to_instagram
from .render import render_template, create_image
from .words import get_word_and_data

MAX_OVERALL_TRIES = 10


def main_process_flow(instagram_post, open_file):
    """Generate image based on random word and definition."""
    word, definitions = get_word_and_data()
    render = render_template(word, definitions)
    image = create_image(render)
    if instagram_post:
        post_to_instagram(image, caption="")
    if open_file:
        subprocess.run(["xdg-open", image])
    return image


def main_process_handling(instagram_post=False, open_file=False):
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
            result = main_process_flow(instagram_post, open_file)
        except Exception as e:
            logging.exception(e)
            time.sleep(2)  # wait after getting exception
            continue
        finally:
            tries += 1
    logging.info("End of run")


def generate_and_open():
    """Generate definition image and open file without posting to instagram."""
    main_process_handling(open_file=True)


def generate_and_post():
    """Generate definition image and post to instagram."""
    main_process_handling(instagram_post=True)
