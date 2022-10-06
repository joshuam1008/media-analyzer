from inference import make_prediction

# import random
# import time

# sys.path.append("../../src")


class SentimentModule:
    @classmethod
    def generate_result(cls, content):
        """Returns value of sentiment for tweet content. 0: Negative, 1: Neutral, 2: Positive"""
        result = make_prediction(content)  # time.sleep(2.4)
        return result["emo"]  # random.randint(-1, 1)
