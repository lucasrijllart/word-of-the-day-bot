# Word Of The Day bot

![Tests](https://github.com/lucasrijllart/word-of-the-day-bot/workflows/Tests/badge.svg?branch=main)

Post daily word definitions on social media.

Twitter account: https://twitter.com/WordOfTheDay_B

## Introduction

The goal of this project is to create a bot that posts a "word of the day" style update,
which contains a random word and its definition.

The main process flow is the following:
  1. Retrieve a random word and its definition through the use of a 3rd-party API
  2. Generate an HTML page with the retrieved data using a template
  3. Render the HTML page into an image
  4. Post the image to social media

The social media posts are performed every day through the [Twitter schedule](https://github.com/lucasrijllart/word-of-the-day-bot/actions?query=workflow%3A%22Twitter+schedule%22) Action

## Local development

Create or workon the virual environment:

`workon word-of-the-day`

Install dependencies using requirments file:

`pip install -r requirements.txt`

Run unit tests:

`python -m unittest discover tests/unit/`

Generate a new image and open it (Ubuntu only):

`generate_and_open`
