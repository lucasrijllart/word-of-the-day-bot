Word of the day bot

Saw the merriam-webster instagram feed https://www.instagram.com/merriamwebster/ and it
inspired me to think about the difficulty of implementing something similar in a very
limited amount of time.

Went for a browse around https://rapidapi.com to learn more about it and see if it could
be useful for this project. Once I found an API that provides random words and their
definitions I was fuelled to start this project.

The start was planning the steps that were needed. The quick draft was the following:

1. Retrieve word and definitions
2. Generate pretty image with text
3. Post to social media

The journey


1. Random word def
Analysis of api endpoints and how to authenticate

RapidAPI provides an easy way to authenticate with any API from their website. They
provide you with a token that is valid on all the APIs you want to use from their site.

To construct the interface with their endpoint, I divided the code into a few parts:
the request maker, the parser, and the retry handler. The API would sometimes return a
word without a definition (if the word is rare or constructed of multiple words) therefore
it would try many times to get a definition before giving up. To facilitate debugging, 
every response from their API is saved to a file with a timestamp so analysing issues is easy.


2. Template rendering

I wanted to easily represent the data in a beautiful manner which could easily posted to social media.
My instict told me to use HTML as it's easy to create templates for text structure, and also easy to change the
colours/styles to improve scaling to multiple social medias to obey their colour scheme.

For the fonts, I found the Google Font API to be very simple to interact with.

The challenge was finding a way to convert an HTML page to an image. I thought there would be very rudamentary
methods involving a browser and screenshots, but after some research I found wkhtmltopdf (link).
It offered a command-line interface `wkhtmltoimage` to perform just that conversion given a width and height.

Jinja2 for templating, done a quick edit for that

(quick example of template body)


3. Testing, splitting of modules and packaging

Tests directory, unit testing the logic mostly. As many of the functions I defined were
for process flow. Included some functional tests to ensure the connection to the WordsAPI
was successful.

CI:
Github action to run tests

Split modules into the following:
1. entry points: run the program with different configurations
2. main: contains the overall process handling functions to kick off the program
3. words: handling WordsAPI integration to retrieve a word and definition
4. render: generating the HTML page from a template and rendering it into an image
5. instagram: handling Instagram integration for posting images


4. Instagram integration

Investigated options, created template, created account, first post, then banned
https://github.com/ohld/igbot

Very simple code
def post(image_path, caption):
     """Posts an image to instagram."""
     username = getenv("INSTAGRAM_USERNAME")
     password = getenv("INSTAGRAM_PASSWORD")
     if not username or not password:
         raise Exception("Instagram username/password could not be retrieved from env.")
     bot = Bot()
     bot.login(username=username, password=password)
     bot.upload_photo(image_path, caption=caption)

5. Move to twitter
Twitter library research, twitter dev account, testing


6. Github actions
Using artifacts to store information for debugging

Then iterative approach at creating workflows:
a. generate
b. generate and post
c. schedule post
d. post checker


<a class="twitter-timeline" data-lang="en" data-width="500" data-height="800" data-theme="dark" href="https://twitter.com/WordOfTheDay_B?ref_src=twsrc%5Etfw">Tweets by WordOfTheDay_B</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
