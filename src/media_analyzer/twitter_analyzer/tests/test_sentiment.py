from django.test import TestCase
import sys

# Add module to path
sys.path.append('../twitter_analyzer')
from twitter_analyzer.views import stream_cache, data_base

# Add parent module to path
sys.path.append('../twitter_analyzer/tasks')

from twitter_analyzer.tasks import get_sentiment


# Create your tests here.
# Adapted from https://test-driven-django-development.readthedocs.io/en/latest/03-views.html#the-homepage-test

class TestSentiment(TestCase):
    '''
    test sentiment storing and access
    '''
    def test_valid_value_generation(self): 
        id = "1"
        text = "TEST TEXT ONE"

        # Put an item into the stream cache
        stream_cache.put({'id': id, 'text': text})

        get_sentiment(stream_cache=stream_cache, db=data_base)

        result_object = stream_cache.get()
        sentiment = result_object['sentiment']
        valid_value = sentiment == 1 or sentiment == 0 or sentiment == -1
        self.assertTrue(valid_value)
