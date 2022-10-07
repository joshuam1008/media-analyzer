# twitter streaming module
import os
import tweepy
from twitter_analyzer.models import Tweet
from queue import Queue
from filters.filter import Filter

"""
Inherit from Tweepy's StreamingClinet to override filter, on_tweet, on_connect, etc.
"""


class TwitterStream(tweepy.StreamingClient):
    """Subclass of Tweepy's StreamingClient. Overrides important method and used as an interface for
    getting and processing actual tweets."""

    def __init__(self):
        """Initialize the Stream."""
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
            bearer_token=os.getenv("BEAR_TOKEN")
        )  # "AAAAAAAAAAAAAAAAAAAAAOn9awEAAAAAq3TgEs2AfsyDjyzdSXoho1hZqWs%3DiXFD8nUBNu7OPF7xBv2hBr0QTmx4KEew911vvyWA2S5kxJosAL"

    """
    Get status
    0 means stopped
    1 means running
    -1 means paused
    """

    def get_status(self):
        """Get the current status of the stream- whether it's running, paused, or connected."""
        if self.is_connected:
            return 1 if not self.is_paused else -1
        else:
            return 0

    def toggle_module(self):
        """
        Connect to stream if not connected. Disconnect the stream otherwise.
        """
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

    def on_tweet(self, tweet):
        """Put a tweet into the timeline from the stream.
        Automatically called when stream gets a tweet."""
        # put into queue if stream is not paused
        if not self.is_paused:
            self.timeline.put(Tweet(tweet))
        # end stream
        if not self.is_connected:
            self.disconnect()

    # things to do when connect to stream
    def on_connect(self):
        """Run when the stream connects.
        Log a message to let us know we're connected."""
        print("connected to stream\n")

    # things to do when disconnect to stream
    def on_disconnect(self):
        """Run when the stream disconnects.
        Log a message to let us know we're disonnected."""
        print("connected to stream\n")
        self.is_connected = False
        print("disconnected")

    def on_exception(self):
        """Run when the stream throws an exception.
        Disconnect the stream and set appropriate flags."""
        self.disconnect()
        self.is_connected = False
        print("Disconnected by Twitter.")

    def pause_resume(self):
        """Toggles whether stream is paused or not."""
        self.is_paused = not self.is_paused

    def result_generator(self):
        """
        Gets all tweets from the current timeline and returns them as serialized objects.
        """
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
