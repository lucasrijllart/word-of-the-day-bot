"""Render text into a visual image."""
from datetime import date, datetime
import subprocess

from jinja2 import Template


COLOR_SCHEMES = {
    "born": {
        "background_color": "#8FC1E3",
        "date_color": "#687864",
        "word_color": "black",
        "definition_color": "#31708E",
    },
    "elegant_yet_approachable" = {
        "background_color": "#EEE2DC",
        "date_color": "#AC3B61",
        "word_color": "black",
        "definition_color": "#123C69",
    }
}

TEMPLATE_FILE = "template_1.html"


def get_date():
    """Get and format date to comfortable style. Example: Monday 1st of January 2020."""
    day = date.today().day
    mapping = {1: "st", 2: "nd", 3: "rd"}
    suffix = 'th' if 11 <= day <= 13 else mapping.get(day % 10, 'th')
    return date.today().strftime("%A %d{S} of %b %Y").replace("{S}", suffix)


def render_template(word, definitions):
    """Render an HTML template with the new word and definitions."""
    data = {
        "todays_date": get_date(),
        "word": word,
        "definitions": definitions,
        **COLOR_SCHEMES["elegant_yet_approachable"],
    }

    with open(TEMPLATE_NAME, "r") as file:
        template = Template(file.read())
    html = template.render(**data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    render_name = f"render_{timestamp}.html"
    with open(render_name, "w") as f:
        f.write(html)
    print("rendered:", render_name)
    return render_name


def create_image(input_file, output_file):
    """Create image from given HTML file."""
    # can add "-q"
    args = [
        "wkhtmltoimage", "--height", "1000", "--width", "1000", input_file, output_file
    ]
    subprocess.run(args)
    print(f"created {output_file} from {input_file}")
    return output_file
