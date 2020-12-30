"""Module handling Twitter integration to post media."""
import logging
import os

from TwitterAPI import TwitterAPI

from .utils import timestamp


def authenticate_api():
    """Authenticate with TwitterAPI library using env vars."""
    logging.info("Authenticating with Twitter API")
    consumer_key = os.environ["TWITTER_API_KEY"]
    consumer_secret = os.environ["TWITTER_API_SECRET_KEY"]
    access_token_key = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TOKEN_SECRET"]
    api = TwitterAPI(
        consumer_key, consumer_secret, access_token_key, access_token_secret,
        #api_version="2"
    )
    return api


def tweet_image(caption, file_path, data_dir=None):
    """Post a tweet with given image and caption."""
    api = authenticate_api()

    logging.info("Starting media upload")
    with open(file_path, "rb") as file:
        image_data = file.read()
    media_upload_response = api.request("media/upload", None, {"media": image_data})

    if data_dir:
        file_name = f"twitter_response_{timestamp()}"
        with open(os.path.join(data_dir, file_name), "w") as file:
            file.write(media_upload_response.text)
        logging.info("TwitterAPI response file %s saved" % file_name)

    if media_upload_response.status_code == 200:
        logging.info("Twitter media upload successful")
    else:
        logging.exception(media_upload_response.__dict__)
        raise Exception("Twitter media upload unsuccessful!")

    logging.info("Starting status update")
    media_id = media_upload_response.json()["media_id"]
    data = {"status": caption, "media_ids": media_id}
    tweet_response = api.request("statuses/update", data)

    if tweet_response.status_code == 200:
        logging.info("Twitter post successful")
    else:
        logging.exception(tweet_request.__dict__)
        raise Exception("Twitter post unsuccessful!")

    url = tweet_response.json().get("entities").get("media")[0].get("expanded_url")
    logging.info("Twitter post url: %s" % url)
    return url
