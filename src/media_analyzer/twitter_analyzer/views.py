from django.shortcuts import render
from streams.twitter_stream import stream
from django.http import JsonResponse
import json
import twitter_analyzer.tasks as tasks
from queue import Queue
from twitter_analyzer.scheduler import background_scheduler
scheduler = background_scheduler.background_scheduler
# module status
modules_status = {"stream": True, "sentiment": False,
                  "topic": False, "lang": False}
# simulate databse
data_base = {}
# a cache stream over 2 secs period to alleviate call to database
stream_cache = Queue()


def cache_stream(stream_cache, scheduler):
    """Gets the results from the stream and puts them into the cache."""
    stream_new_entries = stream.result_generator()
    for entry in stream_new_entries:
        tweet = {'id': entry[0], 'text': entry[1]}
        tasks.process_tweet_by_category(modules_status, tweet, stream_cache)
    # scheduler next one when this one finished
    scheduler.add_job(cache_stream, kwargs={
                      'stream_cache': stream_cache, 'scheduler': scheduler})


def clear_cache(stream_cache, db):
    """
    clear stream cache and copy to database
    stream_cache:Queue
    db:used a dictionary for database for now.
    """
    # save to db and clear cache
    while not stream_cache.empty():
        data = stream_cache.get()
        stream_cache.task_done()
        for key in data.keys():
            if key == "id":
                continue
            if data["id"] not in db:
                db[data["id"]] = {}
            db[data["id"]][key] = data[key]


def send_result(request):
    """
    API end point to return processed result and stream.
    """
    if request.method == "POST":
        # De-Serialize Request to a Python Object
        packet = json.load(request)
        # TODO: consider convert id and category to lower case and remove duplication for security
        categories = packet["category"]
        # toggle model
        for category in categories:
            modules_status[category] = True
        ids = packet["id"]
        fetched_result = {"stream": [], "inds": []}
        # fetch result from stream first if requested
        if "stream" in categories:
            fetched_result["stream"] = fetch_from_stream(categories)
        # fetch result in db
        fetched_result["inds"] = fetch_from_db(ids, categories)
        return JsonResponse(fetched_result)


def fetch_from_stream(categories):
    """
    fetch result from stream by categories
    stream data alwasy has text data,
    if data not exist, schedule to generate it
    """

    # remove stream from category
    categories.remove("stream")
    fetched_result = {}
    for _ in range(stream_cache.qsize()):
        data = stream_cache.get()
        id = data["id"]
        # put text in first for stream
        fetched_result[id] = {"text": data["text"]}
        for category in categories:
            # if result exist fetch
            if category in data:
                fetched_result[id][category] = data[category]
            # schedule to generate the result
            else:
                # None value tell the frontend try again later
                fetched_result[id][category] = None
        stream_cache.task_done()
        # put back to stream
        stream_cache.put(data)
    return fetched_result


def fetch_from_db(ids, categories):
    """
    fetch result from db,
    if data not exist, schedule to generate it
    """
    fetched_result = {}
    for id in ids:
        # check if database has this entry
        if id not in data_base:
            continue
        for category in categories:
            fetched_result[id] = {}
            # fetch if exist
            if category in data_base[id]:
                fetched_result[id][category] = data_base[id][category]
            # schedule to generate the result
            else:
                fetched_result[id][category] = None
                scheduler.add_job(tasks.process_id_by_category, kwargs={
                    "categories": modules_status, 'id': id, "db": data_base
                })
    return fetched_result


def index(request):
    """
    The only page for this application
    """
    return render(request, "twitter_analyzer/index.html")


def rest_module():
    """
    Periodically shuts down the model to reduce consumption.
    """
    print("shutting down module")
    for key in modules_status.keys():
        modules_status[key] = False


if scheduler is not None:
    # start process on stream data
    scheduler.add_job(clear_cache, 'interval', seconds=2, kwargs={
                      'stream_cache': stream_cache, 'db': data_base})
    scheduler.add_job(cache_stream, kwargs={
                      'stream_cache': stream_cache, 'scheduler': scheduler})
    # scheduler.add_job(rest_module, 'interval', minutes=5)
    scheduler.start()
else:
    # check apps.py for init
    print("scheduler not initalized, check if the apps.py been set correctly")
