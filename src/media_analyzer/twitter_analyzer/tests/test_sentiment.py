from django.test import TestCase
from twitter_analyzer.views import stream_cache, data_base
from twitter_analyzer.tasks import get_sentiment

# Add module to path
# sys.path.append("../twitter_analyzer")

# Add parent module to path
# sys.path.append("../twitter_analyzer/tasks")


# Create your tests here.
# Adapted from https://test-driven-django-development.readthedocs.io/en/latest/03-views.html#the-homepage-test


class TestSentiment(TestCase):
    """
    test sentiment storing and access
    """

    def test_valid_value_generation_cache(self):
        """Manually puts a value into the stream cache. Ensure the sentiment generated has
        the correct type."""
        id = "1"
        text = "TEST TEXT ONE"
        # Put an item into the stream cache
        stream_cache.put({"id": id, "text": text})

        get_sentiment(stream_cache=stream_cache, db=data_base)

        result_object = stream_cache.get()
        while (not stream_cache.empty()) and result_object["id"] != id:
            self.assertIsNone(result_object.get("sentiment"))
            result_object = stream_cache.get()
        sentiment = result_object.get("sentiment")
        self.assertTrue(
            (sentiment == "NEUTRAL")
            or (sentiment == "POSITIVE")
            or (sentiment == "NEGATIVE")
        )

    def test_valid_value_generation_db(self):
        """Manually put a value into the database. Ensure the sentiment generated has
        the correct type."""
        id = "2"
        text = "TEST TEXT TWO"

        # Put an item into the database
        data_base[id] = {"id": id, "text": text}

        get_sentiment(stream_cache=stream_cache, id="2", db=data_base)

        result_object = data_base[id]
        sentiment = result_object.get("sentiment")
        self.assertTrue(
            (sentiment == "NEUTRAL")
            or (sentiment == "POSITIVE")
            or (sentiment == "NEGATIVE")
        )
