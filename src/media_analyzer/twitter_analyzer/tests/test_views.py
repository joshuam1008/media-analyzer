from django.test import TestCase
from django.test import Client
import json
import time
from twitter_analyzer.scheduler import background_scheduler 
from streams.twitter_stream import stream
# Create your tests here.
# Adapted from https://test-driven-django-development.readthedocs.io/en/latest/03-views.html#the-homepage-test
"""
mimic user behavior testing views and api
"""


class TestViews(TestCase):
    def setUp(self):
    
        self.client = Client()  # Django's TestCase already sets self.client so this line isn't required


    """Tests the routing/URLs of the site."""

    def test_homepage(self):
        """Tests the homepage URL."""
        response = self.client.get("/twitter/")
        self.assertEqual(response.status_code, 200)
    """Test stream api"""
    def test_stream(self):
        time.sleep(1)  # wait for the server
        response = self.client.post('/twitter/fetch_result', {"id": [], "category": ['stream']})
        stream = json.loads(response.content)
        print("recieved")
        print(stream)
        self.assertTrue(len(stream['stream'].keys()) != 0)




    """Put at buttom to end other thread"""
    def test_wrap_up(self):
        background_scheduler.stop_scheduler()
        stream.disconnect()
        stream.worker.join()
        self.assertTrue(background_scheduler.background_scheduler is None)

    # def test_stream(self):
    #     time.sleep(1)  # wait for the server
    #     response = self.client.post('/twitter/fetch_result', {"id": [], "category": ['stream']})
    #     stream = json.loads(response.content)
    #     print("recieved")
    #     print(stream)
    #     self.assertTrue(len(stream['stream'].keys()) != 0)

    # def test_sentiment(self):
    #     python_dict = {"id": [], "category": ['stream']}
    #     response = self.client.post('/twitter/fetch_result/',
    #                                 json.dumps(python_dict),
    #                                 content_type="application/json")
    #     data = json.loads(response)
    #     stream = data['stream']
    #     id = stream.keys()[0]
    #     python_dict = {"id": [id], "category": ['sentiment']}
    #     response = self.client.post('/twitter/fetch_result/',
    #                                 json.dumps(python_dict),
    #                                 content_type="application/json")
    #     sentiment = json.loads(response)['inds'][id]['sentiment']
    #     self.assertTrue(sentiment != "NEGATIVE" or sentiment !=
    #                     "NEUTRAL" or sentiment != "POSITIVE")