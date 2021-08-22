# Word of the day bot

## Introduction

One day, while browsing Instagram, I found the [Merriam-Webster Instagram account](
https://www.instagram.com/merriamwebster/) which posts beautiful pictures along with
a word and its definition every day. It made me think about how hard it would be to
implement something similar (and simpler) in a very limited amount of time.

In the rest of this page, I write about the journey from an idea to a fully-working
prototype along with the challenges faced, and expanding it past MVP stage. Read
along to see how less than two weeks turned into this Twitter account:

<a class="twitter-timeline" data-lang="en" data-width="500" data-height="800" data-theme="dark" href="https://twitter.com/WordOfTheDay_B?ref_src=twsrc%5Etfw">Tweets by WordOfTheDay_B</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

The first challenge I thought of was around finding random words and definitions.
I went for a browse around https://rapidapi.com to see if an API that provides
words and definitions already existed. With no surprise, I quickly found one that did
just that, and that's how I was motivated to start this project.

I started planning the steps that were needed. The following is a quick summary of the
daily process:
1. Get a random word and its definitions
2. Generate a pretty image with the retrieved text
3. Post it to social media


## Random words and definitions

The story beings around the [RapidAPI](https://rapidapi.com) website. The site provides
an easy way to authenticate with many different APIs: they provide you with a token that is
valid on all the APIs you want to use.
The requirements for this step were simple, I needed to receive a random word and its
definitions upon request. The message format did not matter as long as I could easily
retrieve both.

I found [WordsAPI](https://rapidapi.com/dpventures/api/wordsapi/) rapidly, here is the
summary of their JSON API:
> Words API lets you retrieve information about English words, including definitions,
synonyms, rhymes, pronunciation, syllables, and frequency of usage. It also can tell
you about relationships between words, for instance that “math” has categories like
“algebra” and “geometry”, or that a “finger” is part of a “hand”.

I did some analysis of the API endpoints it offers, authenticated with the service, and
started receiving random words and definitions.

The following is an example response from their API.

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

To construct the interface with their endpoint, I divided the code into a few parts:
the request maker, the response parser, and the retry handler. WordsAPI would sometimes return a
word without a definition (if the word is rare or constructed of multiple words),
therefore I made the program try many times to get a definition before giving up. To
facilitate debugging, every response from their API is saved to a file with a timestamp,
so analysing issues is made easy.


## Image generation

After having the data for the random word and definition, the next step was to create
an image that could be posted to social media. This also meant having some flexibility
on style, which would help posting to different social medias with a different theme. The
requirements therefore were:
- to generate an image on command
- the image had to obey to a certain template schema to follow design rules like
  spacing, colours, and fonts
- the image had to be of specific size to follow social media guidelines and
  recommendations

After reflecting on these requirements my instict pointed be towrads HTML. That language
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
screenshots, but after a lot of research I found [wkhtmltopdf]. It offered a command-line
interface `wkhtmltoimage` to perform just that conversion given a width and height.

The cli is used in the following way to convert a certain `template.html` file into an
image `render.jpg`:
``` sh
wkhtmltoimage --width "400" --height "400" template.html render.jpg
```

After this process, the program successfully turned some text into a simple image.

[Google Font API]: https://developers.google.com/fonts/docs/developer_api
[wkhtmltopdf]: https://wkhtmltopdf.org/


## Testing, code architecture, and process flow

Like with any software project, one of the most important aspects supporting integrity
and resilience is strong testing. Testing, in this case, means unit tests for code
quality, functional testing for process strength, and continuous integration for
rapid feedback of bug introduction.

I split the repository to include a tests directory that contained unit tests, mostly for
checking the logic. As many of the functions I defined were for process flow, 
I included some functional tests to ensure the connection to the WordsAPI was successful
and that the entrypoints to the program were available too.

For continuous integration (CI) I wrote a Github action that runs the tests at every new
commit pushed (more on Actions later). This ensured that a new piece of functionality wouldn't break existing
functionality by regression testing features.

I split modules into the following:
1. entrypoints: run the program with different configurations
2. main: contains the overall process handling functions to kick off the program
3. words: handling WordsAPI integration to retrieve a word and definition
4. render: generating the HTML page from a template and rendering it into an image


## Instagram integration

Now that we have a beautiful image, it needs to be posted to social media.

Originally, I wanted to make this application post to Instagram just like the
Merriam-Webster account. I did some reading around Instagram bots and APIs, but at the
time of coding there was no official API to use. I found multiple articles pointing to
unofficial libraries and tools that can be used, but every time there were lots of warnings
such as: "This is an unofficial library, use at your own risk". Many comments were made online
about how Instagram was actively banning bot accounts using unofficial APIs.

I found the following library and decided to give it a go: https://github.com/ohld/igbot.
I created a quick Instagram template for the picture I wanted to post, then wrote the
integration code, which was quite simple. Here is what it looked like:

``` py
def instagram_post(image_path, caption):
     """Posts an image to instagram."""
     username, password = getenv("INSTAGRAM_USERNAME"), getenv("INSTAGRAM_PASSWORD")
     if not username or not password:
         raise Exception("Instagram username/password could not be retrieved from env.")
     bot = Bot()
     bot.login(username=username, password=password)
     bot.upload_photo(image_path, caption=caption)
```

I ran the above code and it succeeded! A single image, describing what a "swamp maple" is,
was posted to the Instagram account I created: https://www.instagram.com/word_of_the_day_bot/.
Unfortunately, a few hours later, I received an email explaining that my account access had been
limited due to "suspicious activity". I therefore could not post to the account anymore and
was, in other words, banned. This discouraged me from posting to Instagram, given their
website explicitely stated they wanted Instagram to remain a human-only mobile-only
experience.

However, in 2021 [Facebook announced it was introducing content publishing using the Facebook
Graph API](
https://developers.facebook.com/blog/post/2021/01/26/introducing-instagram-content-publishing-api/).
This is the same as the Facebook Graph API but for the picture-only social
media. See https://developers.facebook.com/products/instagram/apis/ for more information.
This API could be explored to enhance the WOTD bot to post to multiple social medias.


## Twitter integration

After the disappointing ban on my new Instagram account, I ventured down the Twitter path.
The Twitter Developer site is simple and efficient, setting up an account was quick, and
the available actions, APIs, and libraries were intuitive. They offer a public API which
can be accessed by a large number of approved third-party libraries for your language of
choice. I went with the first Python library and got started writing the integration code.
See the library here: https://github.com/geduldig/TwitterAPI.

A subtlety of the Twitter API is that it does not allow a tweet with media directly. The
media (image, in this case) needs to be uploaded to Twitter on its own, then it can be
referenced in the tweet. This was accomplished easily by wrapping those two library calls
into different Python functions.

The library worked wonders and the tweets were appearing on the account perfectly. This
worked for a few days, until one day, Twitter restricted my app. I contacted their
Support team multiple times, raising multiple tickets. They unblocked it at first, claiming
it was a mistake. A few days later it was restricted again and so I had to chase their team
again. This back and forth went on for a few months until I received an explanation that
an automated system "disables abusive API keys in bulk" and my application was caught in this.

[image]

Once I managed to get my application unblocked again, I made sure to re-gerenate the API key,
so that it wouldn't be caught in this process again. I found this quite stupid, given that the
API key is generated by Twitter in the first place, so it doesn't make sense to
then scour the keys they've generated and disable "abusive" ones. Anyway, after changing my key
the Twitter integration worked perfectly.


## Scheduled posting

Now that the program could post a new image to Twitter with the click of a button (the enter key, when running the program), 
I needed a way to automatically run it. [Github actions](https://github.com/features/actions) were the obvious choice for this, as they can be run on a schedule.
Actions also support the creation and storage of [artifacts](https://docs.github.com/en/actions/guides/storing-workflow-data-as-artifacts), which would normally be a package or binary file to be used after being built. However, these allow
any files to be stored, so I decided to save all the files generated during the process for easy debugging. All files are saved to the `data` folder, it contains:
1. The WordsAPI response(s) received
2. The HTML file created
3. The JPG file generated from the HTML file
4. The two (or more) Twitter responses from uploading the image and creating the post

I found it easiest to create the Github Action workflow files by using an iterative approach, as these can only be tested by running them in Github so it results in many runs. The
workflow file went through the following iterations:
1. Build: generic Python workflow build file with latest Ubuntu image, Pip, and then installed requirements.txt
2. Build, then run a Python entrypoint from the setup.py
3. Build, generate image using entrypoint
4. Build, generate image and save as artifact
5. Build, generate image, post to Twitter, and save artifact
6. Run action on a schedule

I found that scheduled Actions aren't always on time, so this couldn't be used for Production-level timings, however, for this usage it was appropriate. The timing
also did tend to improve over time, the first few runs could be hours late. After a while it started running only a few minutes late.


## Conclusion

Overall, this project went very smoothly. The number of tools and libraries that are available nowadays have made the development of most things a case of wiring up the right things together. I will try to keep this project working in the future. Some dependencies will need upgrading, and Twitter application credentials will need to be updated. If the program cannot successfully post to Twitter, the Github Action fails and I get alerted via an email.

If you have any questions about the project, please contact me.

You can find all the source code on my Github page: https://github.com/lucasrijllart/word-of-the-day-bot/
