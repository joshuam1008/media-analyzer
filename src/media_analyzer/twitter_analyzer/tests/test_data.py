from django.test import TestCase
from django.test import Client
from train import data
import pandas as pd

# Create your tests here.
# Adapted from https://test-driven-django-development.readthedocs.io/en/latest/03-views.html#the-homepage-test
"""
mimic user behavior testing views and api
"""


class TestData(TestCase):
    def test_process_text(self):
        test_df = pd.DataFrame([['0', '@Connor @Michael Hello world', 'positive']])
        test_df.columns = ['textID', 'text', 'sentiment']
        filtered = data.data_preprocess(test_df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
        self.assertTrue(filtered.at[0, 'text'] == 'Hello world')

    def test_process_text_multiple(self):
        test_df = pd.DataFrame([['0', '@Connor @Michael Hello world', 'positive'],
        ['1', '@Connor Hello world two', 'negative'],
        ['2', '@Connor @Michael @Username Hello world three', 'neutral']])
        test_df.columns = ['textID', 'text', 'sentiment']
        filtered = data.data_preprocess(test_df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
        self.assertTrue((filtered.at[0, 'text'] == 'Hello world') and 
        (filtered.at[1, 'text'] == 'Hello world two') and 
        (filtered.at[2, 'text'] == 'Hello world three'))

    def test_process_sentiment(self):
        test_df = pd.DataFrame([['0', '@Connor @Michael Hello world', 'positive']])
        test_df.columns = ['textID', 'text', 'sentiment']
        filtered = data.data_preprocess(test_df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
        self.assertTrue(filtered.at[0, 'sentiment'] == [0, 0, 1.0])

    def test_process_sentiment_multiple(self):
        test_df = pd.DataFrame([['0', '@Connor @Michael Hello world', 'positive'],
        ['1', '@Connor Hello world two', 'negative'],
        ['2', '@Connor @Michael @Username Hello world three', 'neutral']])
        test_df.columns = ['textID', 'text', 'sentiment']
        filtered = data.data_preprocess(test_df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
        self.assertTrue((filtered.at[0, 'sentiment'] == [0, 0, 1.0]) and
        (filtered.at[1, 'sentiment'] == [1.0, 0, 0]) and
        (filtered.at[2, 'sentiment'] == [0, 1.0, 0]))

    def test_empty(self):
        test_df = pd.DataFrame(columns=['textID', 'text', 'sentiment'])
        filtered = data.data_preprocess(test_df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
        self.assertTrue(filtered.shape[0] == 0)

    def test_wrong_encodings(self):
        test_df = pd.DataFrame([['0', '@Connor @Michael Hello world', 'positive'],
        ['1', '@Connor Hello world two', 'negative'],
        ['2', '@Connor @Michael @Username Hello world three', 'neutral']])
        test_df.columns = ['textID', 'text', 'sentiment']
        
        with self.assertRaises(Exception) as cm:
            data.data_preprocess(test_df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1})
        except_message = str(cm.exception)
        self.assertEqual(except_message, 'Length of label_encoding does not match number of labels')

    def test_wrong_text_col_sen(self):
        test_df = pd.DataFrame([['0', '@Connor @Michael Hello world', 'positive'],
        ['1', '@Connor Hello world two', 'negative'],
        ['2', '@Connor @Michael @Username Hello world three', 'neutral']])
        test_df.columns = ['textID', 'text', 'sentiment']

        with self.assertRaises(Exception) as cm:
            data.data_preprocess(test_df, 'text', 'sentimentS', 3, {'negative':0, 'neutral':1, 'positive':2})
        except_message = str(cm.exception)
        self.assertEqual(except_message, 'sentimentS not in dataframe columns')

    def test_wrong_text_col(self):
        test_df = pd.DataFrame([['0', '@Connor @Michael Hello world', 'positive'],
        ['1', '@Connor Hello world two', 'negative'],
        ['2', '@Connor @Michael @Username Hello world three', 'neutral']])
        test_df.columns = ['textID', 'text', 'sentiment']
        
        with self.assertRaises(Exception) as cm:
            data.data_preprocess(test_df, 'textT', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
        except_message = str(cm.exception)
        self.assertEqual(except_message, 'textT not in dataframe columns')

    def test_bad_df(self):
        test_df = None
        with self.assertRaises(Exception) as cm:
            data.data_preprocess(test_df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
        except_message = str(cm.exception)
        self.assertEqual(except_message, 'df must be DataFrame, not None')


if __name__=='__main__':
    t = TestData()
    t.test_process_text()
    t.test_process_text_multiple()
    t.test_process_sentiment()
    t.test_process_sentiment_multiple()
    t.test_empty()
    t.test_wrong_encodings()
    t.test_wrong_text_col_sen()
    t.test_wrong_text_col()
    t.test_bad_df()