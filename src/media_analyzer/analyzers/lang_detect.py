import random
import time 
class LangModule():
    @classmethod
    def generate_result(cls,content=None):
        lang_index = random.randint(0,3)
        langs = ['en','cn','aa','bb']
        return langs[lang_index]