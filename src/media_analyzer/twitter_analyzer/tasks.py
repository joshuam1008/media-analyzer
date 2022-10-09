"""
For celery to handle task in async way
"""
from celery import shared_task
from analyzers.sentiment_module import SentimentModule
from analyzers.topic_module import TopicModule
from analyzers.lang_detect import LangModule


@shared_task()
def get_sentiment(stream_cache=None, id=None, db=None):
    """
    Get sentiment results for stream or for ind tweets with id.
    """
    # generate result for stream first
    if id is None:
        for _ in range(stream_cache.qsize()):
            data = stream_cache.get()
            stream_cache.task_done()
            if "sentiment" not in data:
                data["sentiment"] = SentimentModule.generate_result(
                    data["text"])
            stream_cache.put(data)

    # generate result for ids and store to db
    else:
        if db[id].get("sentiment", None) is None:
            db[id]["sentiment"] = SentimentModule.generate_result(
                db[id]["text"])


@shared_task()
def get_topic(stream_cache, ids, db):
    """
    get topic label for stream or for ind tweets with id
    """
    # generate result for stream first
    for _ in range(stream_cache.qsize()):
        data = stream_cache.get()
        stream_cache.task_done()
        if "topic" not in data:
            data["topic"] = TopicModule.generate_result(data["text"])
        stream_cache.put(data)

    # generate result for ids
    # TODO


@shared_task()
def get_lang(stream_cache, id=None, db=None):
    """
    get lang result for stream or for ind tweets with id
    """
    # generate result for stream first
    for _ in range(stream_cache.qsize()):
        data = stream_cache.get()
        stream_cache.task_done()
        if "lang" not in data:
            data["lang"] = LangModule.generate_result(data["text"])
        stream_cache.put(data)

    # generate result for ids
    # TODO


@shared_task()
def process_tweet_by_category(categories, tweet: dict, stream_cache):
    """Returns the result of a given category (sentiment, topic, language, etc.) of the given ids
    within the stream cache."""
    # generate result for stream first
    if categories["sentiment"]:
        tweet['sentiment'] = SentimentModule.generate_result(tweet['text'])
    if categories['lang']:
        tweet['lang'] = LangModule.generate_result(tweet['text'])
    stream_cache.put(tweet)


@shared_task()
def process_id_by_category(categories, id: int, db):
    '''
    process tweet with this id by categories and store the result in db
    '''
    tweet = db[id]
    if categories['sentiment']:
        tweet[tweet['sentiment']] = SentimentModule.generate_result(
            tweet['text'])
    if categories['lang']:
        tweet[tweet['lang']] = LangModule.generate_result(tweet['text'])
    db[id] = tweet
