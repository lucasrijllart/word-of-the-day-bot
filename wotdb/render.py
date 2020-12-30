"""Render text into a visual image."""
from datetime import date
import logging
from os import path
import subprocess

from jinja2 import Template

from . import templates as templates_folder
from .utils import timestamp


def _format_date(the_date=date.today()):
    """Get and format date to comfortable style. Example: Monday 1st of January 2020."""
    mapping = {1: "st", 2: "nd", 3: "rd"}
    suffix = 'th' if 11 <= the_date.day <= 13 else mapping.get(the_date.day % 10, 'th')
    return the_date.strftime("%A %-d{S} of %B %Y").replace("{S}", suffix)


def _format_definitions(data):
    result = ""
    for index, values in data.items():
        if len(data) < 2:
            result += f"{values['part']}: {values['definition']}"
        else:
            result += f"<sup>{index}</sup> {values['part']}: {values['definition']}"
        if int(index) != len(data):
            result += "</br>"
    return result


def _render_template(word, definitions, data_dir, template_name):
    """Render an HTML template with the new word and definitions."""
    logging.info("Using template: %s" % template_name)
    template_path = path.join(templates_folder.__path__[0], template_name)
    with open(template_path, "r") as file:
        template = file.read()

    data = {
        "todays_date": _format_date(),
        "word": word,
        "definitions": _format_definitions(definitions),
    }
    html = Template(template).render(**data)

    render_name = f"render_{timestamp()}.html"
    render_path = path.join(data_dir, render_name)
    with open(render_path, "w") as file:
        file.write(html)
    logging.info("Rendered HTML file: %s" % render_name)
    return render_path


def _create_image(render_path, data_dir):
    """Create image from given HTML file."""
    logging.info("Starting html to image conversion")
    image_name = f"image_{timestamp()}.jpg"
    image_path = path.join(data_dir, image_name)

    args = [
        "xvfb-run", "wkhtmltoimage", "--height", "1000", "--width", "1000",
        render_path, image_path
    ]
    subprocess.run(args)

    try:
        f = open(image_path)
    except FileNotFoundError:
        raise Exception("Image was not created!")
    else:
        logging.info("Created image %s" % image_name)
    finally:
        f.close()

    return image_path


def create_image_from_template(word, definitions, data_dir, template_name):
    """Create image from rendered HTML template."""
    render_path = _render_template(word, definitions, data_dir, template_name)
    image_path = _create_image(render_path, data_dir)
    return image_path
