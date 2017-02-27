#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import tweepy
import os
import requests
from PIL import Image
from io import open as iopen

# Get the data from the Met Office
data = requests.get("https://api.ffc-environment-agency.fgs.metoffice.gov.uk/api/public/statements").json()

# Get the most recent statment
most_recent = 0
for statement in data["statements"]:
   if statement["id"] > most_recent:
      most_recent = statement["id"]
recent_statement = requests.get("https://api.ffc-environment-agency.fgs.metoffice.gov.uk/api/public/statements/"+str(most_recent)).json()

# Get the text
forecast_text = recent_statement["statement"]["headline"]

if len(forecast_text) > 114:
   forecast_text = forecast_text[:114] + u"…\n"

# Get the image
forecast_image_url = recent_statement["statement"]["png_thumbnails_with_days_url"]

# Save Image
photo_path = 'forecast_image.png'
image = requests.get(forecast_image_url)
with iopen(photo_path, 'wb') as file:
   file.write(image.content)

# Replace alpha with white
png = Image.open(photo_path)
png.load() # required for png.split()
background = Image.new("RGB", png.size, (255, 255, 255))
background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
background.save(photo_path, 'PNG')

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

status = forecast_text + "\n" + info_url

#print status

api.update_with_media(photo_path, status=status)
os.remove(photo_path)
