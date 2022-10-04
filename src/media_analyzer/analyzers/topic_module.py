import random
import time 
class TopicModule():
    @classmethod
    def generate_result(cls,content=None):
        topic_index = random.randint(0,3)
        topics = ['topic1','topic2','topic3','topic4']
        return topics[topic_index]