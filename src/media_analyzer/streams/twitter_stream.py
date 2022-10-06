# twitter streaming module
from concurrent.futures import thread
import tweepy
from src.media_analyzer.twitter_analyzer.models import Tweet
from queue import Queue
from src.media_analyzer.filters.filter import Filter
import os

# customize the stream filter method
class TwitterStream(tweepy.StreamingClient):
    def __init__(self):
        self.worker = None
        self.timeline: "Queue[Tweet]" = Queue()
        self.connection_flag = False
        self.pause_flag = True
        super().__init__(bearer_token=os.getenv("BEAR_TOKEN"))

    """
    Get status
    0 meanse stoped
    1 means running
    -1 means paused 
    """

    def get_status(self):
        if self.connection_flag:
            return 1 if not self.pause_flag else -1
        else:
            return 0

    """
    Connect to stream if not connected. Disconnet the stream otherwise
    """

    def toggle_module(self):
        self.connection_flag = not self.connection_flag
        # create worker and start the stream
        if self.connection_flag:
            self.pause_flag = False
            self.worker = self.sample(threaded=True)
        # join thread and stop stream
        else:
            self.pause_flag = True
            if self.worker is not None:
                self.worker.join()

    # override the on_tweet method
    def on_tweet(self, tweet):
        # put into queue if stream is not paused
        if not self.pause_flag:
            self.timeline.put(Tweet(tweet))
        # end stream
        if not self.connection_flag:
            self.disconnect()

    # things to do when connect to stream
    def on_connect(self):
        print("connected to stream\n")

    # things to do when disconnect to stream
    def on_disconnect(self):
        print("disconnected")

    def pause_resume(self):
        self.pause_flag = not self.pause_flag

    """
    return all tweet.text have been stored in stream buffer
    filter: a filter function used to filter stream
    """

    def result_generator(self, filters=[]):
        # pour tweets into list
        tmp_results = []
        while not self.timeline.empty():
            tmp_results.append(self.timeline.get())
            self.timeline.task_done()
        results = []
        for tweet in tmp_results:
            result = tweet.text
            add_to_results = True
            for filter in filters:
                # if filter is a Filter object
                if isinstance(filter, Filter):
                    # error handling incase crash
                    try:
                        if not filter.filter(result):
                            add_to_results = False
                            break
                    except:
                        # print out the name of the filter
                        print(f"Error while using {type(filter).__name__}")
            if add_to_results:
                results.append(result)
        return results
