from django.db import models

# Create your models here.
class Tweet():
    def __init__(self,tweet):
        self.tweet = tweet
        self.text = tweet.text
    