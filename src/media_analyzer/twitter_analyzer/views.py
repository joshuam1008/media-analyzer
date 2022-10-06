from django.shortcuts import render
from streams.twitter_stream import TwitterStream
from django.http import JsonResponse
import json
import twitter_analyzer.tasks as tasks
from apscheduler.schedulers.background import BackgroundScheduler
from queue import Queue

# module status
modules_status = {"stream": True, "sentiment": False, "topic": False, "lang": False}
# simulate databse
data_base = {}
# a cache stream over 2 secs period to alleviate call to database
stream_cache = Queue()

# The Stream Object
stream = TwitterStream()

# Start the Stream
stream.toggle_module()

"""
clear stream cache
input Queue: cache
"""


def cache_stream(stream_cache):
    stream_new_entries = stream.result_generator()
    for entry in stream_new_entries:
        entry_id = entry[0]
        entry_text = entry[1]
        stream_cache.put({"id": entry_id, "text": entry_text})


"""
clear stream cache and copy to database
stream_cache:Queue
db:used a dictionary for database now
"""


def clear_cache(stream_cache, db):
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


"""
An event triggered scheduler
category: task name
stream_cache: Queue
ids: ind tweets need to be processed
db: a dictionary, used to represent database for now
"""


def schedule_result_by_category(category, stream_cache, ids, db):
    if category == "sentiment":
        scheduler.add_job(
            tasks.get_sentiment,
            kwargs={"stream_cache": stream_cache, "id": ids, "db": data_base},
        )


"""
scheduler for periodically schedule job
"""


def schedule_job(scheduler):
    if modules_status["sentiment"]:
        scheduler.add_job(
            tasks.get_sentiment,
            kwargs={"stream_cache": stream_cache, "id": None, "db": None},
        )
    if modules_status["topic"]:
        scheduler.add_job(
            tasks.get_topic,
            kwargs={"stream_cache": stream_cache, "ids": None, "db": None},
        )
    if modules_status["lang"]:
        scheduler.add_job(
            tasks.get_lang,
            kwargs={"stream_cache": stream_cache, "ids": None, "db": None},
        )
    if modules_status["stream"]:
        scheduler.add_job(
            clear_cache, kwargs={"stream_cache": stream_cache, "db": data_base}
        )
        scheduler.add_job(cache_stream, kwargs={"stream_cache": stream_cache})


"""
API end point to return processed result and stream
"""


def send_result(request):
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


"""
fetch result from stream by categories
stream data alwasy has text data,
if data not exist, schedule to generate it
"""


def fetch_from_stream(categories):
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
                schedule_result_by_category(category, stream_cache, None, None)
        stream_cache.task_done()
        # put back to stream
        stream_cache.put(data)
    return fetched_result


"""
fetch result from db,
if data not exist, schedule to generate it
"""


def fetch_from_db(ids, categories):
    fetched_result = {}
    for id in ids:
        # check if database has this entry
        if id not in data_base:
            continue
        print("reached")
        for category in categories:
            fetched_result[id] = {}
            # fetch if exist
            if category in data_base[id]:
                fetched_result[id][category] = data_base[id][category]
            # schedule to generate the result
            else:
                fetched_result[id][category] = None
                schedule_result_by_category(category, stream_cache, id, data_base)
    return fetched_result


"""
The only page for this application
"""


def index(request):
    results = []
    tweets = []
    for _ in range(stream_cache.qsize()):
        result = stream_cache.get()
        stream_cache.task_done()
        stream_cache.put(result)
        results.append(result)

    for result in results:
        tweets.append(result["text"])
    return render(request, "twitter_analyzer/index.html", {"tweets": tweets})


"""
rest module to save consumption
"""


def rest_module():
    print("shutting down module")
    for key in modules_status.keys():
        modules_status[key] = False


# init scheduler
scheduler = BackgroundScheduler()
# schedule job
scheduler.add_job(schedule_job, "interval", seconds=2, kwargs={"scheduler": scheduler})
scheduler.add_job(rest_module, "interval", minutes=5)
scheduler.start()
