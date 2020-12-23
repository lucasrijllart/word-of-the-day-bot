"""Render text into a visual image."""
from datetime import date, datetime
import logging
from os import path
import subprocess

from jinja2 import Template

from . import templates as templates_folder
from . import data as data_folder


COLOR_SCHEMES = {
    "born": {
        "background_color": "#8FC1E3",
        "date_color": "#687864",
        "word_color": "black",
        "definition_color": "#31708E",
    },
    "elegant_yet_approachable": {
        "background_color": "#EEE2DC",
        "date_color": "#AC3B61",
        "word_color": "black",
        "definition_color": "#123C69",
    }
}

TEMPLATE_1 = "template_1.html"

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

TEMPLATES_FOLDER = templates_folder.__path__[0]
DATA_FOLDER = data_folder.__path__[0]


def _get_date():
    """Get and format date to comfortable style. Example: Monday 1st of January 2020."""
    day = date.today().day
    mapping = {1: "st", 2: "nd", 3: "rd"}
    suffix = 'th' if 11 <= day <= 13 else mapping.get(day % 10, 'th')
    return date.today().strftime("%A %d{S} of %B %Y").replace("{S}", suffix)


def _format_definitions(data):
    result = ""
    for index, values in data.items():
        if len(data) < 2:
            result += f"{values['part']}: {values['definition']}"
        else:
            result += f"<sup>{index}</sup>{values['part']}: {values['definition']}"
        if int(index) != len(data):
            result += "</br>"
    return result


def render_template(word, definitions, template_name=TEMPLATE_1):
    """Render an HTML template with the new word and definitions."""
    data = {
        "todays_date": _get_date(),
        "word": word,
        "definitions": _format_definitions(definitions),
        **COLOR_SCHEMES["elegant_yet_approachable"],
    }

    template_path = path.join(TEMPLATES_FOLDER, template_name)
    with open(template_path, "r") as file:
        template = Template(file.read())
    html = template.render(**data)

    render_name = f"render_{TIMESTAMP}.html"
    render_path = path.join(DATA_FOLDER, render_name)
    with open(render_path, "w") as file:
        file.write(html)
    logging.info("Rendered HTML file: %s" % render_name)
    return render_path


def create_image(render_path):
    """Create image from given HTML file."""
    image_name = f"image_{TIMESTAMP}.jpg"
    image_path = path.join(DATA_FOLDER, image_name)
    args = [
        "wkhtmltoimage", "-q", "--height", "1000", "--width", "1000",
        render_path, image_path
    ]
    subprocess.run(args)
    logging.info("created %s from %s" % (image_name, render_path.rsplit("/", 1)[-1]))
    return image_path
