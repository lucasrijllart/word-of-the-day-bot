"""Module handling Twitter integration to post media.

Library used: https://github.com/geduldig/TwitterAPI
"""
import logging
import os

from TwitterAPI import TwitterAPI

from .utils import timestamp


class Twitter():
    """Class holding Twitter integration functionality."""

    def __init__(self, data_dir):
        """Store directory path for file saving and authenticate with Twitter creds."""
        self.data_dir = data_dir
        self.api = self._authenticate_api()

    def _authenticate_api(self):
        """Authenticate with TwitterAPI library using env vars."""
        logging.info("Authenticating with Twitter API")
        consumer_key = os.environ["TWITTER_API_KEY"]
        consumer_secret = os.environ["TWITTER_API_SECRET_KEY"]
        access_token_key = os.environ["TWITTER_ACCESS_TOKEN"]
        access_token_secret = os.environ["TWITTER_TOKEN_SECRET"]
        return TwitterAPI(
            consumer_key, consumer_secret, access_token_key, access_token_secret
        )

    def _media_upload(self, file_path):
        """Upload an image to Twitter, to be later referenced in a tweet."""
        logging.info("Starting media upload")
        with open(file_path, "rb") as file:
            image_data = file.read()
        response = self.api.request("media/upload", None, {"media": image_data})

        if self.data_dir:
            file_name = f"twitter_response_{timestamp()}"
            with open(os.path.join(self.data_dir, file_name), "w") as file:
                file.write(response.text)
            logging.info("TwitterAPI media/upload response file %s saved" % file_name)

        if response.status_code == 200:
            logging.info("Twitter media upload successful")
        else:
            logging.exception(response.__dict__)
            raise Exception("Twitter media upload unsuccessful!")

        return response.json()["media_id"]


    def _statuses_update(self, caption, media_id):
        """Compose tweet with caption and image."""
        logging.info("Starting status update")
        data = {"status": caption, "media_ids": media_id}
        response = self.api.request("statuses/update", data)
        
        if self.data_dir:
            file_name = f"twitter_statuses_update_response_{timestamp()}"
            with open(os.path.join(self.data_dir, file_name), "w") as file:
                file.write(response.text)
            logging.info("TwitterAPI statuses/update response file %s saved" % file_name)

        if response.status_code == 200:
            logging.info("Twitter post successful")
        else:
            logging.exception(tweet_response.__dict__)
            raise Exception("Twitter post unsuccessful!")

        url = response.json().get("entities").get("media")[0].get("expanded_url")
        logging.info("Twitter post url: %s" % url)
        return url


    def tweet_image(self, caption, file_path):
        """Post a tweet with given caption and image."""
        media_id = self._media_upload(file_path)
        url = self._statuses_update(caption, media_id)
        return url
