from django.test import TestCase
import time
from streams.twitter_stream import TwitterStream
from twitter_analyzer import views


# Add module to path
# sys.path.append("../twitter_analyzer")


"""
IMPORTANT: Class uses bearer token to initialize new stream. This counts towards the limits
imposed by the twitter stream API. Don't run this test too much.
"""


class TestStream(TestCase):
    """
    Tests the Twitter Stream.
    """

    def test_stream_responses(self):
        """Tests opening a stream, getting some data, and ensuring the type. """

        # Disconnect Other stream running in view
        views.stream.disconnect()

        # Initialize the Stream
        stream = TwitterStream()

        # Start the Stream
        stream.toggle_module()

        # Wait for Results
        time.sleep(10)

        # Check if we were disconnected
        if stream.is_connected:
            # Disconnect the Stream
            stream.disconnect()

            # Get Results of Stream.
            results = stream.result_generator()

            # Ensure we got something.
            self.assertTrue(len(results) > 0)

            # Ensure we got strings.
            first_result = results[0][1]
            print(first_result)
            self.assertTrue(isinstance(first_result, str))
        else:
            print("Disconnected By Twitter")
