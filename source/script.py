"""

username: lucas.rijllart@hotmail.com
password: <in lastpass>
https://rapidapi.com/dpventures/api/wordsapi/endpoints


https://www.geeksforgeeks.org/post-a-picture-automatically-on-instagram-using-python/
https://pypi.org/project/instabot/
"""
from datetime import date
import json
from subprocess import run

from jinja2 import Template
import requests

BASE_API = "https://wordsapiv1.p.rapidapi.com/"

HEADERS = {
    "x-rapidapi-key": "8d02058f51msh5f15d59c4557d70p13503cjsn19946f965c3b",
    "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
    "useQueryString": "true",
}

MAX_TRIES = 10


def get_random_word():
    """Gets random word from API."""
    random_word_endpoint = BASE_API + "words/?random=true"
    response = requests.get(random_word_endpoint, headers=HEADERS)
    data = json.loads(response.text)
    return data["word"]


def get_definitions(word):
    """Gets definition and part of speech description of given word."""
    definition_endpoint = f"{BASE_API}words/{word}/definitions"
    response = requests.get(definition_endpoint, headers=HEADERS)
    data = json.loads(response.text)
    return data["definitions"]


def get_text():
    
    def format_definition(definition):
        print(definition)
        return definition["partOfSpeech"] + ": " + definition["definition"]

    word = get_random_word()
    print(word)

    definitions_result = get_definitions(word)
    # definitions = [definition["definition"] for definition in definitions]
    # part_of_speech = [definition["partOfSpeech"] for definition in definitions]
    if definitions_result and len(definitions_result) > 1:
        definitions = ""
        for index, definition in enumerate(definitions_result[:3]):
            print(definition, index)
            formatted = format_definition(definition)
            definitions += f"<sup>{index}</sup>{formatted}<br>"
    elif definitions_result and len(definitions_result) == 1:
        definitions = format_definition(definitions_result[0])
    else:
        definitions = None
    print("def:", definitions)
    return word, definitions


def render_template(word, definitions):
    """Render an HTML template with the new word and definitions."""
    today = date.today()
    mapping = {1: "st", 2: "nd", 3: "rd"}
    suffix = 'th' if 11<=today.day<=13 else mapping.get(today.day%10, 'th')
    todays_date = today.strftime("%A %d{S} of %b %Y").replace("{S}", suffix)
    data = {
        "todays_date": todays_date,
        "word": word,
        "definitions": definitions,
    }

    color_scheme_born = {
        "background_color": "#8FC1E3",
        "date_color": "#687864",
        "word_color": "black",
        "definition_color": "#31708E",
    }
    color_scheme_original = {
        "background_color": "#EEE2DC",
        "date_color": "#AC3B61",
        "word_color": "black",
        "definition_color": "#123C69",
    }
    template_name = "template.html"
    kwargs = {
        **color_scheme_original,
        **data,
    }
    template_name = "template.html"
    with open(template_name, "r") as file:
        template = Template(file.read())
    html = template.render(**kwargs)

    render_name = "render.html"
    with open(render_name, "w") as f:
        f.write(html)
    print("rendered:", render_name)
    return render_name


def transform_to_image(input_file, output_file):
    """Transform given html file to an image format."""
    args = ["wkhtmltoimage", "-q", "--height", "1000", "--width", "1000", input_file, output_file]
    run(args)
    print(f"transformed {input_file} to {output_file}")
    return output_file



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
    transform_to_image(render, output_file)
    return output_file

main()
run(["xdg-open", "output.jpg"])


# simple - too many definitions, not good
