from langdetect import detect


class LanguageFilter():
    """Filter for filtering content by a language"""

    def __init__(self, language="en"):
        """Created a LanguageFilter for given language. Default language is 'en'."""
        super().__init__()
        self.language = language

    @classmethod
    def filter(cls, content):
        """Return the language label, return error if can't detect"""
        language = None
        try:
            language = detect(content)
        except:
            language = "error"
        return language
