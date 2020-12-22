"""Render text into a visual image."""
from os import path
from datetime import date, datetime
import subprocess

from jinja2 import Template

import templates as templates_folder
import data as data_folder

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
    return date.today().strftime("%A %d{S} of %b %Y").replace("{S}", suffix)


def render_template(word, definitions, template_name=TEMPLATE_1):
    """Render an HTML template with the new word and definitions."""
    data = {
        "todays_date": _get_date(),
        "word": word,
        "definitions": definitions,
        **COLOR_SCHEMES["elegant_yet_approachable"],
    }

    template_path = path.join(TEMPLATES_FOLDER, template_name)
    with open(template_path, "r") as file:
        template = Template(file.read())
    html = template.render(**data)

    render_path = path.join(DATA_FOLDER, f"render_{TIMESTAMP}.html")
    with open(render_path, "w") as file:
        file.write(html)
    print("rendered:", render_path)
    return render_path


def create_image(render_path):
    """Create image from given HTML file."""
    # can add "-q" based on the logs
    image_name = f"image_{TIMESTAMP}.jpg"
    image_path = path.join(DATA_FOLDER, image_name)
    args = [
        "wkhtmltoimage", "--height", "1000", "--width", "1000", render_path, image_path
    ]
    subprocess.run(args)
    print(f"created {image_name} from {render_path.rsplit('/', 1)}")
    return image_path
