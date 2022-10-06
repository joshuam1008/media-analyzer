# twitter streaming module
import tweepy
from twitter_analyzer.models import Tweet
from queue import Queue
from filters.filter import Filter

"""
Inherit from Tweepy's StreamingClinet to override filter, on_tweet, on_connect, etc.
"""


class TwitterStream(tweepy.StreamingClient):
    def __init__(self):
        # subscribe filters
        self.subscription = {}
        self.worker = None
        self.timeline: "Queue[Tweet]" = Queue()

        # True when stream is connected, false when disconnected.
        self.is_connected = False

        # True when stream is paused.
        self.is_paused = True

        # Initialize class with authorization
        super().__init__(
            bearer_token="AAAAAAAAAAAAAAAAAAAAAOn9awEAAAAAq3TgEs2AfsyDjyzdSXoho1hZqWs%3DiXFD8nUBNu7OPF7xBv2hBr0QTmx4KEew911vvyWA2S5kxJosAL"
        )  # os.getenv("BEAR_TOKEN"))

    """
    Get status
    0 means stopped
    1 means running
    -1 means paused
    """

    def get_status(self):
        if self.is_connected:
            return 1 if not self.is_paused else -1
        else:
            return 0

    """
    Connect to stream if not connected. Disconnect the stream otherwise
    """

    def toggle_module(self):
        self.is_connected = not self.is_connected
        # create worker and start the stream
        if self.is_connected:
            self.is_paused = False
            self.worker = self.sample(threaded=True)
        # join thread and stop stream
        else:
            self.is_paused = True
            if self.worker is not None:
                self.worker.join()

    # override the on_tweet method
    def on_tweet(self, tweet):
        # put into queue if stream is not paused
        if not self.is_paused:
            self.timeline.put(Tweet(tweet))
        # end stream
        if not self.is_connected:
            self.disconnect()

    # things to do when connect to stream
    def on_connect(self):
        print("connected to stream\n")

    # things to do when disconnect to stream
    def on_disconnect(self):
        self.is_connected = False
        print("disconnected")

    def on_exception(self):
        self.disconnect()
        self.is_connected = False
        print("Disconnected by Twitter.")

    def pause_resume(self):
        self.is_paused = not self.is_paused

    """
    return list of all tweet.text have been stored in stream buffer
    filter: a filter function used to filter stream
    """

    def result_generator(self):
        # pour tweets into list
        raw_tweets = []
        while not self.timeline.empty():
            raw_tweets.append(self.timeline.get())
            self.timeline.task_done()
        results = []
        for tweet in raw_tweets:
            add_to_results = True
            for filter in self.subscription.values():

                # if filter is a Filter object
                if isinstance(filter, Filter):
                    # error handling incase crash
                    try:
                        if not filter.filter(tweet.get_content()):
                            add_to_results = False
                            break
                    except Exception:
                        # print out the name of the filter
                        print(f"Error while using {type(filter).__name__}")
            if add_to_results:
                results.append([tweet.get_id(), tweet.get_content()])
        return results
