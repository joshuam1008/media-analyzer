#twitter streaming module 
import tweepy
from twitter_analyzer.models import Tweet
from queue import Queue
from filters.filter import Filter
#customize the stream filter method
class TwtterStream(tweepy.StreamingClient):
    
    def __init__(self,bear_token):
        self.timeline: "Queue[Tweet]" = Queue()
        self.connection_flag = True
        self.pause_flag = False
        super().__init__(bearer_token=bear_token)
    
    def on_tweet(self,tweet):
        #put into queue if stream is not paused
        if not self.pause_flag:
            self.timeline.put(Tweet(tweet))
            self.timeline.task_done()
        #end stream 
        if not self.connection_flag:
            self.disconnect()
    
    def on_connect(self):
        print("connected to stream\n")
        self.pause_flag = False
        self.connection_flag = True
    
    def on_disconnect(self):
        print("disconnected")
        self.pause_falg = True
        self.connection_flag = False

    def pause_stream(self):
        self.pause_flag = True
    
    def resume_stream(self):
        self.pause_flag = False
    
    def stop_stream(self):
        self.connection_flag = False
    
    """
    return all tweet.text have been stored in stream buffer
    filter: a filter function used to filter stream
    """
    def result_generator(self,filters=[]):
        results = []
        while not self.timeline.empty():
            result = self.timeline.get().text
            self.timeline.task_done()
            add_to_results = True
            for filter in filters:
                #if filter is a Filter object
                if isinstance(filter,Filter):
                    #error handling incase crash
                    try:
                        if not filter.filter(result):
                            add_to_results = False
                            break
                    except:
                        #print out the name of the filter
                        print(f'Error while using {type(filter).__name__}')
            if add_to_results:
                results.append(result)
        return results
    
    