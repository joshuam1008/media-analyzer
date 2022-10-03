from django.db import models

# Create your models here.
class Tweet():
    def __init__(self,tweet):
        
        self.tweet = tweet
        self.text = tweet.text
        self.id = tweet.id_str
    
    def get_content(self):
        return self.tweet.text
    
    def get_id(self):
        return self.tweet.id_str