"""Package initialisation. Holds main function."""
import subprocess

from render import render_template, create_image
from words import get_word_and_definitions

MAX_OVERALL_TRIES = 10
MAX_DEFINITION_TRIES = 15


def main_process():
    """Run the whole process post a new word to instagram."""
    word, definitions = get_word_and_definitions()
    if not definitions:
        tries = 0
        while not definitions and tries < MAX_DEFINITION_TRIES:
            word, definitions = get_word_and_definitions()
            tries += 1
        if tries == MAX_TRIES:
            raise Exception("Too many attempts to define words with empty results.")

    render = render_template(word, definitions)
    image = create_image(render)
    return image


def run():
    """Handle any exceptions from main process and just retry."""
    result = None
    tries = 0
    while not result and tries < MAX_OVERALL_TRIES:
        try:
            result = main_process()
        except:
            continue
        tries += 1
    print("Finished:", result)
    return result


if __name__ == "__main__":
    file = run()
    subprocess.run(["xdg-open", file])
