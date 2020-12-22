"""Package initialisation. Holds main function."""
import subprocess

from render import render_template, create_image
from words import get_word_and_definitions

MAX_TRIES = 15


def run():
    """Run the whole process post a new word to instagram."""
    word, definitions = get_word_and_definitions()
    if not definitions:
        tries = 0
        while not definitions and tries < MAX_TRIES:
            word, definitions = get_word_and_definitions()
            tries += 1
        if tries == MAX_TRIES:
            raise Exception("Too many attempts to define words with empty results.")

    render = render_template(word, definitions)
    image = create_image(render)
    return image


if __name__ == "__main__":
    file = run()
    print("End of run:", file)
    subprocess.run(["xdg-open", file])
