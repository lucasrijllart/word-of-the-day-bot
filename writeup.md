# Word of the day bot

## Introduction

One day, while browsing Instagram, I saw the merriam-webster instagram account
https://www.instagram.com/merriamwebster/ and it made me think about the challenges
involved around implementing something similar in a very limited amount of time. Here's
an example of what I saw that day.

[image]

The first thought I had was around finding random words and definitions. I went for a
browse around https://rapidapi.com to learn more about it and see if it could
be useful for this project. Once I found an API that provides random words and their
definitions I was motivated to start this project.

I started planning the steps that were needed. The quick draft was the following:
1. Get a random word and its definitions
2. Generate a pretty image with text
3. Post it to social media

In the rest of this page, I write about the journey to a fully-working prototype along
with the challenges faced, and expanding it past MVP stage. Read along to see how a few
weeks turned into this Twitter account:

<a class="twitter-timeline" data-lang="en" data-width="500" data-height="800" data-theme="dark" href="https://twitter.com/WordOfTheDay_B?ref_src=twsrc%5Etfw">Tweets by WordOfTheDay_B</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 


## Random words and definitions

The story beings around the https://rapidapi.com website. RapidAPI provides an easy way
to authenticate with many different APIs: they provide you with a token that is
valid on all the APIs you want to use from their site.
The requirements for this step were simple, I needed to receive a random word and its
definitions upon request. The message format did not matter as long as I could easily
retrieve both.

I found [WordsAPI](https://rapidapi.com/dpventures/api/wordsapi/) rapidly, here is the
summary of their API:
> Words API lets you retrieve information about English words, including definitions,
synonyms, rhymes, pronunciation, syllables, and frequency of usage. It also can tell
you about relationships between words, for instance that “math” has categories like
“algebra” and “geometry”, or that a “finger” is part of a “hand”.

I did some analysis of the API endpoints it offers, authenticated with the service, and
started receiving random words and definitions.

To construct the interface with their endpoint, I divided the code into a few parts:
the request maker, the parser, and the retry handler. WordsAPI would sometimes return a
word without a definition (if the word is rare or constructed of multiple words),
therefore I made the program try many times to get a definition before giving up. To
facilitate debugging, every response from their API is saved to a file with a timestamp,
so analysing issues is made easy.

The following is an example response from their API

``` json
{
  "word": "funambulism",
  "results": [
    {
      "definition": "walking on a tightrope or slack rope",
      "partOfSpeech": "noun",
      "synonyms": ["tightrope walking"],
      "typeOf": ["athletics","sport"],
      "derivation": ["funambulist"]
    }
  ],
  "syllables": {
    "count": 4,
    "list": ["fu","nam","bu","lism"]
  }
}
```


## Image generation

After having the data for the random word and definition, the next step was to create
an image which could be posted to social media. This also meant having some flexibility
on style which would help posting to different social medias with a different theme. The
requirements therefore were:
- to generate an image on command
- the image had to obey to a certain template schema to follow design rules like
  spacing, colours, and fonts
- the image had to be of specific size to follow social media guidelines and
  recommendations

After reflecting on these requirements my instict suggested to use HTML. That language
makes it easy to create templates for text structure, and also easy to change the
colours/styles to improve scaling to multiple social medias to obey their colour scheme.
It also is the language of the web so would be appropriate for displaying on websites.

I created a simple HTML template which had colours, spacing, and supported a few places
for text: a date at the top, the word in the middle, and the definition at the bottom.
The template looked like this:

[template]

For the fonts, I found the [Google Font API] to be very simple to interact with.
I used Jinja2 for templating as I had already worked with it and it is extremely simple
to use templating to replace tags with variable text.

Here is an example of the HTML created for our example word:

``` html
<html>
  <head>
    <title>Word-of-the-day-bot</title>
    <style>omitted for simplicity</style>
  </head>

  <body style="background-color: #192734">
    <div class="date"><p style="color: #8899A6">Monday 7th of June 2021</p></div>

    <div class="word"><p style="color: white">funambulism</p></div>

    <div class="definition"><p style="color: #E2E7EA">noun: walking on a tightrope or slack rope</p></div>

  </body>
</html>
```

The HTML part was simple, the challenge was finding a way to convert an HTML page to an
image. I thought there would be very rudamentary methods involving a browser and
screenshots, but after some research I found [wkhtmltopdf]. It offered a command-line
interface `wkhtmltoimage` to perform just that conversion given a width and height.

The cli is used in the following way to convert a certain `template.html` file into an
image `render.jpg`:
``` sh
wkhtmltoimage --width "400" --height "400" template.html render.jpg
```

After this process, we successfully turned some text into a beautiful image.

[Google Font API]: https://developers.google.com/fonts/docs/developer_api
[wkhtmltopdf]: https://wkhtmltopdf.org/


## Testing, project architecture, and process flow

Like with any software project, one of the most important aspects supporting integrity
and resilience is strong testing. Testing, in this case, means unit tests for code
quality, functional testing for process strength, and continuous integration for
rapid feedback of bug introduction.

I split the repository to include a tests directory that container unit tests for
checking the logic mostly. As many of the functions I defined were for process flow, 
I included some functional tests to ensure the connection to the WordsAPI was successful
and that the entrypoints to the program were too.

For continuous integration (CI) I used Github action which ran the tests at every new
commit pushed. This ensured that a new piece of functionality wouldn't break existing
functionality by regression testing features.

I split modules into the following:
1. entry points: run the program with different configurations
2. main: contains the overall process handling functions to kick off the program
3. words: handling WordsAPI integration to retrieve a word and definition
4. render: generating the HTML page from a template and rendering it into an image
5. instagram: handling Instagram integration for posting images


## Instagram integration

Investigated options, created template, created account, first post, then banned https://github.com/ohld/igbot

Very simple code
``` py
def post(image_path, caption):
     """Posts an image to instagram."""
     username = getenv("INSTAGRAM_USERNAME")
     password = getenv("INSTAGRAM_PASSWORD")
     if not username or not password:
         raise Exception("Instagram username/password could not be retrieved from env.")
     bot = Bot()
     bot.login(username=username, password=password)
     bot.upload_photo(image_path, caption=caption)
```

## Twitter integration
Twitter library research, twitter dev account, testing


## Scheduled posting
Now I needed a way to automatically create an image and post it to Twitter. [Github actions]() were the obvious choice for this, as they can be run on a schedule.
Actions also support the creation and storage of [artifacts](), which would normally be a package or binary file to be used after being built. However, these allow
any files to be stored. I decided to save all the files generated during the process for easy debugging. All files are saved to the `data` folder, it contains:
1. The WordsAPI response(s) received
2. The HTML file created
3. The JPG file generated from the HTML file
4. The two Twitter responses from uploading the image and creating the post

I found it easiest to create the workflow files by an iterative process, as these can only be tested by running them in Github so it results in many runs. The
workflow file went through the following iterations:
1. Build: generic Python workflow build file with latest Ubuntu image, Pip, and then installed requirements.txt
2. Build, then run a Python entrypoint from the setup.py
3. Build, generate image using entrypoint
4. Build, generate image and save as artifact
5. Build, generate image, post to Twitter, and save artifact
6. Run action on a schedule

I found that scheduled Actions aren't always on time, so this couldn't be used for Production-level timings, however, for this usage it was appropriate. The timing
did tend to improve over time.
