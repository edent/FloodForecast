#!/usr/bin/env python2.7
import tweepy
import urllib2
import xml.etree.cElementTree as et
import time
import datetime
import os

#       Let's get the data
#xmlData = urllib2.urlopen('http://flooddata.alphagov.co.uk/3df.xml').read()

#       Parse the XML
#xmlTree = et.fromstring(xmlData)

#       Get images and write them to disk
#day1Base64 = xmlTree.find('day1image')

img = urllib2.urlopen("http://apps.environment-agency.gov.uk/flood/3days/Controls/FloodForecast/ImageHandler.ashx?ImageId=1")
fileHandle = open("day1image.png", "wb")
fileHandle.write(img.read())
fileHandle.close()

#day2Base64 = xmlTree.find('day2image')
img = urllib2.urlopen("http://apps.environment-agency.gov.uk/flood/3days/Controls/FloodForecast/ImageHandler.ashx?ImageId=2")
fileHandle = open("day2image.png", "wb")
fileHandle.write(img.read())
fileHandle.close()

#day3Base64 = xmlTree.find('day3image')
img = urllib2.urlopen("http://apps.environment-agency.gov.uk/flood/3days/Controls/FloodForecast/ImageHandler.ashx?ImageId=3")
fileHandle = open("day3image.png", "wb")
fileHandle.write(img.read())
fileHandle.close()

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

#       Get the day names of today, tomorrow, and the day after
day = (24*60)*60
today    = datetime.datetime.fromtimestamp(time.time())
tomorrow = datetime.datetime.fromtimestamp(time.time() + day)
third    = datetime.datetime.fromtimestamp(time.time() + day + day)

#       Set the information URL
info = 'http://apps.environment-agency.gov.uk/flood/3days/125305.aspx'

# Send the tweet with photo
photo_path = 'day1image.png'
status = 'The flood forecast for ' + today.strftime('%A')    + ' is...' + info
api.update_with_media(photo_path, status=status)
os.remove(photo_path)

photo_path = 'day2image.png'
status = 'The flood forecast for ' + tomorrow.strftime('%A') + ' is...' + info
api.update_with_media(photo_path, status=status)
os.remove(photo_path)

photo_path = 'day3image.png'
status = 'The flood forecast for ' + third.strftime('%A')    + ' is... ' + info
api.update_with_media(photo_path, status=status)
os.remove(photo_path)
