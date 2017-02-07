#!/usr/bin/env python2.7
import tweepy
import os
import requests
from PIL import Image
from io import open as iopen

# Get the data from the Met Office
data = requests.get("https://api.ffc-environment-agency.fgs.metoffice.gov.uk/api/public/statements").json()

# Last element is most recent. Get forecast
forecast_text = data["statements"][-1]["public_forecast"]["english_forecast"]

# Get Image
forecast_image_url = data["statements"][-1]["png_thumbnails_with_days_url"]

# Save Image
photo_path = 'forecast_image.png'
image = requests.get(forecast_image_url)
with iopen(photo_path, 'wb') as file:
   file.write(image.content)

# Consumer keys and access tokens, used for OAuth
consumer_key        = ''
consumer_secret     = ''
access_token        = ''
access_token_secret = ''

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Set the information URL
info_url = 'https://flood-warning-information.service.gov.uk/5-day-flood-risk'

# Send the tweet with photo
photo_path = 'forecast_image.png'
status = forecast_text + "\n"  + info_url
api.update_with_media(photo_path, status=status)

# Delete the photo
os.remove(photo_path)
