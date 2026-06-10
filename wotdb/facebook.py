""" Module containing Facebook integration to post media.

Using HTTP requests via the Facebook Graph API. Docs:
https://developers.facebook.com/docs/graph-api
"""
import logging
import os
import time

import requests

from .utils import timestamp


class Facebook():
    """Class holding Facebook integration functionality."""

    def __init__(self, data_dir=None):
        """Retrieve secrets from env and retrieve access token from API."""
        self.data_dir = data_dir  # writes API responses to files if provided
        self.api_version = os.environ.get("FACEBOOK_API_VERSION", "v23.0")
        self.app_id = os.environ["FACEBOOK_APP_ID"]
        self.app_secret = os.environ["FACEBOOK_APP_SECRET"]
        self.user_access_token = os.environ.get(
            "FACEBOOK_USER_ACCESS_TOKEN",
            os.environ.get("FACEBOOK_LONG_LIVED_USER_ACCESS_TOKEN")
        )
        self.page_id = os.environ["FACEBOOK_WOTDB_PAGE_ID"]

    def authenticate(self):
        """Perform necessary authentication with Facebook API."""
        self._extend_user_token()
        self.page_access_token = self._get_page_access_token()

    def _extend_user_token(self):
        """Extend or refresh the user access token to ensure it doesn't expire."""
        logging.info("Checking and extending user access token")
        url = f"https://graph.facebook.com/v23.0/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": self.user_access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            new_token = response.json().get("access_token")
            if new_token:
                self.user_access_token = new_token
                logging.info("User access token extended successfully")
            else:
                logging.warning("Token extend returned no access_token, continuing with existing token")
        else:
            logging.warning("Token extend failed (status %s): %s", response.status_code, response.text[:200])

    def _get_page_access_token(self):
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
            if self.data_dir:
                file_name = f"facebook_response_page_token_{timestamp()}.json"
                with open(os.path.join(self.data_dir, file_name), "w") as file:
                    file.write(response.text)
                logging.info("GraphAPI page token response file %s saved" % file_name)
            raise Exception("Facebook page access token retrieval failed:", response_data)

        return response_data.get("access_token")

    def publish_post(self, caption, image_path):
        """ Publish post to page that includes a photo and caption.
        https://developers.facebook.com/docs/pages/publishing#publish-a-photo
        """
        logging.info("Publishing photo to Facebook page")
        url = f"https://graph.facebook.com/{self.page_id}/photos"
        with open(image_path, "rb") as f:
            file = {"file": f}
            params = {
                "caption": caption,
                "access_token": self.page_access_token,
            }

            response = requests.post(url, params=params, files=file)
        if self.data_dir:
            file_name = f"facebook_response_publish_{timestamp()}.json"
            with open(os.path.join(self.data_dir, file_name), "w") as file:
                file.write(response.text)
            logging.info("GraphAPI publish response file %s saved" % file_name)

        photo_id = response.json().get("id")
        post_id = response.json().get("post_id")
        if response.status_code == 200:
            logging.info("Post successful! Photo ID: %s, post ID: %s" % (photo_id, post_id))
        else:
            raise Exception("Facebook post unsuccessful! Error: %s" % response.text)
        return post_id
