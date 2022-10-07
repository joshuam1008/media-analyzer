import random


class TopicModule:
    """Object used to determine topic of given content. Not implemented yet. """
    @classmethod
    def generate_result(cls, content=None):
        """Determine the topic of given content."""
        topic_index = random.randint(0, 3)
        topics = ["topic1", "topic2", "topic3", "topic4"]
        return topics[topic_index]
