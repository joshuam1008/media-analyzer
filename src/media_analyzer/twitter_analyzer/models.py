# from django.db import models

# Create your models here.
class Tweet:
    def __init__(self, tweet):
        # The tweet object itself. https://github.com/joshuam1008/media-analyzer/wiki/Twitter-Jason
        self.tweet = tweet
        # Text from the tweet.
        self.text = tweet.text
        self.id = tweet.id

    def get_content(self):
        return self.tweet.text

    def get_id(self):
        return self.tweet.id
