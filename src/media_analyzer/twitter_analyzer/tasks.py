'''
For celery to handle task in async way
'''
from celery import shared_task
from analyzers.sentiment_module import SentimentModule
from analyzers.topic_module import TopicModule
from analyzers.lang_detect import LangModule
'''
get sentiment result for stream or for ind tweets with id
'''
@shared_task()
def get_sentiment(stream_cache=None,id=None,db=None):
    #generate result for stream first
    if id is None:
        for _ in range(stream_cache.qsize()):
            data = stream_cache.get()
            stream_cache.task_done()
            if 'sentiment' not in data:
                data['sentiment'] = SentimentModule.generate_result(data['text'])
            stream_cache.put(data)
            
    #generate result for ids and store to db
    else:
        if db[id].get("sentiment",None) is None:
            db[id]['sentiment']=SentimentModule.generate_result(db[id]['text'])
            
'''
get topic label for stream or for ind tweets with id
'''
@shared_task()
def get_topic(stream_cache,ids,db):
    #generate result for stream first
    for _ in range(stream_cache.qsize()):
        data = stream_cache.get()
        stream_cache.task_done()
        if 'topic' not in data:
            data['topic'] = TopicModule.generate_result(data['text'])
        stream_cache.put(data)
        
    #generate result for ids
    #TODO
'''
get lang result for stream or for ind tweets with id
'''
@shared_task()
def get_lang(stream_cache,ids,db):
    #generate result for stream first
    for _ in range(stream_cache.qsize()):
        data = stream_cache.get()
        stream_cache.task_done()
        if 'lang' not in data:
            data['lang'] = LangModule.generate_result(data['text'])
        stream_cache.put(data)
        
    #generate result for ids
    #TODO
#TODO A general method to reduce duplicate code 
@shared_task()
def get_result_by_category(category,stream_cache,ids,db):
    #generate result for stream first
    if category == 'sentiment':
        get_sentiment(stream_cache,ids,db)
    
