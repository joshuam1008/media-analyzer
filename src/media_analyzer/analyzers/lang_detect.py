from langdetect import detect  # import random, import time


class LangModule:
    """ An object used to determine the language of given content. """
    @classmethod
    def generate_result(cls, content=None):
        """Returns language of given content. """
        # lang_index = random.randint(0, 3)
        # langs = ["en", "cn", "aa", "bb"]
        return detect(content)  # langs[lang_index]
