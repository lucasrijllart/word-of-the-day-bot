"""Package initialisation. Holds main function."""
from .render import render_template, create_image
from .words import get_text

def main():
    word, definitions = get_text()
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

main()
run(["xdg-open", "output.jpg"])

