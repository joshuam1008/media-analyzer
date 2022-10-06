from filter import Filter
from langdetect import detect


class LanguageFilter(Filter):
    """Filter for filtering content by a language"""

    def __init__(self, language="en"):
        """Created a LanguageFilter for given language. Default language is 'en'."""
        super().__init__()
        self.language = language

    def filter(self, content):
        """Return true if content matches filter's language"""
        return self.language == detect(content)
