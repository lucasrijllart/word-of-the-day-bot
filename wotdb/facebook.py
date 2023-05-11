import os

import requests

API_VERSION = "v16.0"

def get_page_id(user_access_token):
    """Only used once to get page id linked to my user id"""
    user_id = "lucas.rijllart"
    url = f"https://graph.facebook.com/{user_id}/accounts"
    params = {
       "access_token": user_access_token
    }

    response = requests.get(url, params=params)
    print(response)
    print(response.json())

def get_user_access_token():
    """Used to get a short-term user access token"""
    print("Getting user access token...")
    url = "https://graph.facebook.com/oauth/access_token"
    app_id = os.environ["APP_ID"]
    client_secret = os.environ["FACEBOOK_CLIENT_SECRET"]
    params = {
        "client_id": app_id,
        "client_secret": SECRET,
        "grant_type": "client_credentials",
    }

    response = requests.get(url, params=params)
    print(response)
    print(response.text)
    access_token = response.json().get("access_token")

    return access_token

def get_page_acccess_token(user_access_token):
    """Used to get a page access token to perform page actions."""
    print("Getting page access token...")
    page_id = os.environ["PAGE_ID"]
    url = f"https://graph.facebook.com/{page_id}"
    params = {
        "fields": "access_token",
        "access_token": user_access_token
    }

    response = requests.get(url, params=params)
    print(response)
    print(response.json())
    return response.json().get("access_token")


def get_long_lived_user_access_token(short_lived_token):
    """Used to get a 90-day long user access token. Should be saved in a secret."""
    url = "https://graph.facebook.com/v16.0/oauth/access_token"
    app_id = os.environ["APP_ID"]
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": SECRET,
        "fb_exchange_token": short_lived_token,
    }

    response = requests.get(url, params=params)
    print(response)
    print(response.json())

def upload_photo_to_album(user_access_token):
    """Not working"""
    print("Uploading photo to album...")
    file_path = "/Users/lucasrijllart/workspace/word-of-the-day-bot/wotdb/data/test_image.jpg"
    album_id = os.environ["ALBUM_ID"]
    url = f"https://graph.facebook.com/{album_id}/photos"
    params = {
        "caption": "test",
        "url": open(file_path, "rb"),
        "access_token": user_access_token,
    }

    response = requests.post(url, params=params)
    print(response)
    print(response.json())

def publish_post_with_photo_to_page(page_access_token, caption="test"):
    """ Publish post to page that includes a photo and caption.
    https://developers.facebook.com/docs/pages/publishing#publish-a-photo
    """
    print("Publishing photo to page...")
    file_path = "/Users/lucasrijllart/workspace/word-of-the-day-bot/wotdb/data/test_image.jpg"
    page_id = os.environ["PAGE_ID"]
    url = f"https://graph.facebook.com/{page_id}/photos"
    files = {"file": open(file_path, "rb")}
    params = {
        "caption": caption,
        "access_token": page_access_token,
    }

    response = requests.post(url, params=params, files=files)
    print(response)
    print(response.json())  

def create_photo(user_access_token):
    """ Not working
    Docs: https://developers.facebook.com/docs/graph-api/reference/photo#Creating
    """
    print("Creating session to upload image...")
    file_path = "/Users/lucasrijllart/workspace/word-of-the-day-bot/wotdb/data/test.jpg"
    url = f"https://graph.facebook.com/{APP_ID}/uploads"
    params = {
        "file-length": 3931542,
        "file-type": "image/jpg",
        "access_token": user_access_token,
    }

    response = requests.post(url, params=params)
    print(response)
    print(response.json())

    upload_session_id = response.json().get("id")

    print("Uploading image...")
    url = f"https://graph.facebook.com/{upload_session_id}"
    headers = {
        "Authorization": f"Oauth {user_access_token}",
        "file_offset": "0",
    }
    files = {"upload_file": open(file_path,"rb")}
    response = requests.post(url, headers=headers, files=files)

    print(response)
    print(response.json())



# get_long_lived_user_access_token(ACCESS)

# user_access_token = get_user_access_token()
# get_page_id(LONG_LIVED_TOKEN)
user_access_token = os.environ["FACEBOOK_LONG_LIVED_USER_ACCESS_TOKEN"]
page_access_token = get_page_acccess_token(user_access_token)
 
#create_photo(LONG_LIVED_TOKEN)

publish_post_with_photo_to_page(page_access_token)