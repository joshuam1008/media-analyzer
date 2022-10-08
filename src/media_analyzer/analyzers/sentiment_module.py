from analyzers.inference import make_prediction


class SentimentModule:
    """Object used to determine sentiment of given content, using ML model."""

    @classmethod
    def generate_result(cls, content):
        """Returns value of sentiment for tweet content. NEGATIVE, NEUTRAL, POSITIVE, or error if cannot be determined"""
        try:
            result = make_prediction(content)["emo"]
        except Exception:
            result = "error"  # sentiment cannot be determined
        return result
