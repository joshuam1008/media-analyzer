from django.test import TestCase
import time, sys

# Add module to path
sys.path.append('../twitter_analyzer')
from streams.twitter_stream import TwitterStream

# IMPORTANT: Class uses bearer token to initialize new stream. This counts towards the limits
# imposed by the twitter stream API. Don't run this test too much.
class TestStream(TestCase):
    '''
    Tests the Twitter Stream.
    '''
    def test_stream_responses(self):

        # Initialize the Stream
        stream = TwitterStream()

        # Start the Stream
        stream.toggle_module()

        # Wait for Results
        time.sleep(10)

        # Check if we were disconnected
        if stream.running:
            # Disconnect the Stream
            stream.disconnect()

            # Get Results of Stream.
            results = stream.result_generator()

            # Ensure we got something.
            self.assertTrue(len(results) > 0)

            # Ensure we got strings.
            first_result = results[0]
            self.assertTrue(isinstance(first_result, str))
        else:
            print("Disconnected By Twitter")
