from django.test import TestCase
from django.test import Client

# Create your tests here.
# Adapted from https://test-driven-django-development.readthedocs.io/en/latest/03-views.html#the-homepage-test
"""
mimic user behavior testing views and api
"""


class TestViews(TestCase):
    """Tests the routing/URLs of the site."""
    def test_homepage(self):
        """Tests the homepage URL."""
        client = Client()
        response = client.get("/twitter/")
        self.assertEqual(response.status_code, 200)
