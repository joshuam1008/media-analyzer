from django.db import models

# Create your models here.
class Tweet():
    def __init__(self,tweet):
        # The tweet object itself. https://github.com/joshuam1008/media-analyzer/wiki/Twitter-Jason
        self.tweet = tweet

        # Text from the tweet. 
        self.text = tweet.text

        # The id of the tweet as a string.
        self.id_str = tweet.id_str

    