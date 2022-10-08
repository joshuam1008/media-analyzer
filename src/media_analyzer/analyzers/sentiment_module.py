from analyzers.inference import make_prediction


class SentimentModule:
    """Object used to determine sentiment of given content, using ML model."""

    @classmethod
    def generate_result(cls, content):
        """Returns value of sentiment for tweet content. NEGATIVE, NEUTRAL, or POSITIVE"""
        try:
            result = make_prediction(content)["emo"]
        except Exception:
            result = "NEUTRAL"  # if sentiment cannot be determined, default fo neutral
        return result
