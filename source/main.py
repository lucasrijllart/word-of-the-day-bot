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
            word, definitions = get_text()
            tries += 1
        if tries == MAX_TRIES:
            raise Exception("Too many attempts to define words with empty results.")

    render = render_template(word, definitions)
    output_file = "output.jpg"
    create_image(render, output_file)
    return output_file


if __name__ == "__main__":
    file = run()
    subprocess.run("xdg-open", file)
