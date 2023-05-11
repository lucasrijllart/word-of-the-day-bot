""" Module containing Facebook integration to post media.

Using HTTP requests via the Facebook Graph API. Docs:
https://developers.facebook.com/docs/graph-api
"""
import logging
import os

import requests


class Facebook():
    """Class holding Facebook integration functionality."""

    def __init__(self):
        """Retrieve secrets from env and retrieve access token from API."""
        self.api_version = os.environ.get("FACEBOOK_API_VERSION", "v16.0")
        self.user_access_token = os.environ["FACEBOOK_LONG_LIVED_USER_ACCESS_TOKEN"]
        self.page_id = os.environ["FACEBOOK_WOTDB_PAGE_ID"]
    
    def authenticate(self):
        """Perform necessary authentication with Facebook API."""
        self.page_access_token = self._get_page_acccess_token()

    def _get_page_acccess_token(self):
        """Used to get a page access token to perform page actions."""
        logging.info("Getting page access token")
        url = f"https://graph.facebook.com/{self.page_id}"
        params = {
            "fields": "access_token",
            "access_token": self.user_access_token
        }

        response = requests.get(url, params=params)
        response_data = response.json()
        if response.status_code == 200 and "access_token" in response_data:
            logging.info("Page access token retrieved successfully")
        else:
            raise Exception("Facebook page access token retrieval failed:", response_data)

        return response_data.get("access_token")

    def publish_post(self, caption, file_path):
        """ Publish post to page that includes a photo and caption.
        https://developers.facebook.com/docs/pages/publishing#publish-a-photo
        """
        logging.info("Publishing photo to Facebook page")
        url = f"https://graph.facebook.com/{self.page_id}/photos"
        file = {"file": open(file_path, "rb")}
        params = {
            "caption": caption,
            "access_token": self.page_access_token,
        }

        response = requests.post(url, params=params, files=file)
        photo_id = response.json().get("id")
        post_id = response.json().get("post_id")
        if response.status_code == 200:
            logging.info("Post successful! Photo ID: %s, post ID: %s" % photo_id, post_id)
        else:
            raise Exception("Facebook post unsuccessful! Error: %s" % response.text)

def get_long_lived_user_access_token(short_lived_token):
    """Used to get a 90-day long user access token. Should be saved in the secret
    FACEBOOK_LONG_LIVED_USER_ACCESS_TOKEN.
    """
    logging.info("Getting short-lived user access token")
    url = "https://graph.facebook.com/oauth/access_token"
    app_id = os.environ["FACEBOOK_DEV_APP_ID"]
    client_secret = os.environ["FACEBOOK_CLIENT_SECRET"]
    params = {
        "client_id": app_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    response = requests.get(url, params=params)
    if response.status_code == 200 and "access_token" in response.json():
        logging.info("Successfully retrieved short-lived token")
    else:
        raise Exception("Error while retrieving short-lived token")

    short_lived_token = response.json().get("access_token")

    logging.info("Getting long-lived user access token")
    url = "https://graph.facebook.com/v16.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": client_secret,
        "fb_exchange_token": short_lived_token,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        logging.info("Successfully retrieved long-lived token")
    else:
        print(response.text)
        raise Exception("Unsuccessfully retrieved long-lived token!")
    print(response.json())

# user_access_token = get_user_access_token()
# get_page_id(LONG_LIVED_TOKEN)
facebook = Facebook()
facebook.authenticate()
caption = "Test"
file_path = "/Users/lucasrijllart/workspace/word-of-the-day-bot/wotdb/data/test_image.jpg"
facebook.publish_post(caption, file_path)