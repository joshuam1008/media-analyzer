from langdetect import detect  # import random, import time


class LangModule:
    @classmethod
    def generate_result(cls, content=None):
        """Returns language of given content"""
        # lang_index = random.randint(0, 3)
        # langs = ["en", "cn", "aa", "bb"]
        return detect(content)  # langs[lang_index]
