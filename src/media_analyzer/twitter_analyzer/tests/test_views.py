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
        # background_scheduler.start_scheduler()
        # Django's TestCase already sets self.client so this line isn't required
        self.client = Client()
        # stream.toggle_module()
    """Tests the routing/URLs of the site."""
    def tests(self):
        #cap the first letter to avoid been auto executed
        print("test home page")
        self.Test_homepage()
        print("test stream")
        self.Test_stream()
        print("test sentiment")
        self.Test_sentiment()
        print("test lang")
        self.Test_lang()
        #put this at end to stop stand alone threae
        print("closing thread")
        self.Test_wrap_up()

    def Test_homepage(self):
        """Tests the homepage URL."""
        response = self.client.get("/twitter/")
        self.assertEqual(response.status_code, 200)
    
    """Test stream api"""
    def Test_stream(self):
        #try three time 
        for _ in range(3):
            time.sleep(1)
            response = self.client.post('/twitter/fetch_result', json.dumps(
                {"id": [], "category": ['stream']}), content_type='application/json')
            data = response.json()
            self.assertEqual(response.status_code, 200)
            if len(data['stream'].keys()) > 0:
                return True
        return False
    '''Test if backend can generate sentiment'''
    def Test_sentiment(self):
         for _ in range(3):
            time.sleep(1)
            response = self.client.post('/twitter/fetch_result', json.dumps(
                {"id": [], "category": ['stream','sentiment']}), content_type='application/json')
            data = response.json()
            self.assertEqual(response.status_code, 200)
            #check if have sentiment
            for id in data['stream'].keys():
                if 'sentiment' in data['stream'][id]:
                    sentiment = data['stream'][id]['sentiment']
                    if sentiment is not None:
                        if 'NEGATIVE' in sentiment or 'NEUTRAL' in sentiment or 'POSITIVE' in sentiment:
                            return True

         return False
    '''Test if backend can generate language result'''
    def Test_lang(self):
         for _ in range(3):
            time.sleep(1)
            response = self.client.post('/twitter/fetch_result', json.dumps(
                {"id": [], "category": ['stream','lang']}), content_type='application/json')
            data = response.json()
            self.assertEqual(response.status_code, 200)
            #check if have sentiment
            for id in data['stream'].keys():
                if 'lang' in data['stream'][id]:
                    lang_tag = ""
                    lang_tag = data['stream'][id].get('lang',None)
                    if lang_tag is not None:
                        return True
    """Put at buttom to end other thread"""
    def Test_wrap_up(self):
        background_scheduler.stop_scheduler()
        stream.disconnect()
        if stream.worker is not None:
            stream.worker.join()
        self.assertTrue(background_scheduler.background_scheduler is None)
    

