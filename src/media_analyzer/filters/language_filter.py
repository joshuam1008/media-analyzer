from filter import Filter

class LanguageFilter(Filter):
    def __init__(self,language='en'):
        super().__init__()
        self.language = language

    def filter(self,content):
        return True
