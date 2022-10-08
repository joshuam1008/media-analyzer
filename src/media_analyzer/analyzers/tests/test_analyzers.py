from django.test import TestCase
from analyzers import lang_detect, sentiment_module, topic_module


class TestAnalyzers(TestCase):
    """Testing class for 'analyzers' package"""

    def test_lang_detect_valid(self):
        """Gives lang_detect.generate_result a valid string and checks if language is identified correctly"""
        lang = lang_detect.LangModule()

        # english
        en_example = "This is a sentence written in English."
        self.assertEquals("en", lang.generate_result(en_example))

        # chinese
        cn_example = "这是一个用中文来写的句子。"
        self.assertEquals("zh-cn", lang.generate_result(cn_example))

    def test_lang_detect_invalid(self):
        """Gives lang_detect.generate_result invalid string and checks if identified as error correctly"""
        lang = lang_detect.LangModule()
        none_example = None
        empty_example = ""
        self.assertEquals("error", lang.generate_result(none_example))
        self.assertEquals("error", lang.generate_result(empty_example))

    def test_sentiment_module_valid(self):
        """Gives sentiment_module.generate_result valid strings and checks if emotion identified correctly"""
        sent = sentiment_module.SentimentModule()
        positive_example = "Today is a perfectly amazing day!"  # changes in model may affect these, may want to widen test scope
        neutral_example = "This happened 4 days ago."
        negative_example = "Today sucks and is terrible!"
        self.assertEquals("POSITIVE", sent.generate_result(positive_example))
        self.assertEquals("NEUTRAL", sent.generate_result(neutral_example))
        self.assertEquals("NEGATIVE", sent.generate_result(negative_example))

    def test_sentiment_module_invalid(self):
        """Gives sentiment_module.generate_result edge case strings and checks if result is valid"""
        sent = sentiment_module.SentimentModule()
        none_example = None
        empty_example = ""
        weird_text_example = "⏁⊑⟟⌇ ⟟⌇ ⏃ ⌇⟒⋏⏁⟒⋏☊⟒ ⍜⎎ ⍙⟒⟟⍀⎅ ☊⊑⏃⍀⏃☊⏁⟒⍀⌇ ☌⟒⋏⟒⍀⏃⏁⟒⎅ ⏚⊬ ⌇⍜⋔⟒ ⏃⌰⟟⟒⋏ ⌰⏃⋏☌⎍⏃☌⟒ ⍙⟒⏚⌇⟟⏁⟒."  # generated by https://lingojam.com/AlienLanguage
        emotions = ("NEGATIVE", "NEUTRAL", "POSITIVE")
        self.assertEqual("error", sent.generate_result(none_example))
        self.assertIn(sent.generate_result(empty_example), emotions)
        self.assertIn(sent.generate_result(weird_text_example), emotions)

    def test_topic_module(self):
        """Tests that the topic module template had valid return"""
        topic = topic_module.TopicModule()
        topics = ["topic1", "topic2", "topic3", "topic4"]
        self.assertIn(topic.generate_result(), topics)
