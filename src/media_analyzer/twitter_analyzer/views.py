from nis import match
from django.shortcuts import render
from src.media_analyzer.streams.twitter_stream import TwitterStream
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, JsonResponse
import json

# stream = TwitterStream()
# stream.toggle_module()
modules = {"stream": TwitterStream()}
# API for toggling module
"""
API for toggleing module
three signal
-1 pause
0 stop
1 start
the expected json should be 
{'module1 name':signal,'module2 name' signal}
"""


def toggle_module(request):
    if request.method == "POST":
        packet = json.load(request)
        module_name = packet["name"]
        print(module_name)
        state = packet["state"]
        print(state)
        try:
            state = int(state)
        except:
            return HttpResponseServerError("Not a valid operation on the module")
        if module_name not in module_name:
            return HttpResponseServerError("Module doesn't exist")
        else:
            if state == 0 or state == 1:
                modules[module_name].toggle_module()
            elif state == -1:
                modules[module_name].pause_resume()
            else:
                return HttpResponseServerError("Not a valid operation on the module")
    return HttpResponse("")


"""
API for module status
{module_name:status}
-1:paused
0:stoped
1:running
"""


def get_module_status(request):
    status = {}
    for name, module in modules.items():
        status[name] = module.get_status()
    return JsonResponse(status)


# main page
def index(request):
    tweets = modules["stream"].result_generator()
    return render(request, "twitter_analyzer/index.html", {"tweets": tweets})
