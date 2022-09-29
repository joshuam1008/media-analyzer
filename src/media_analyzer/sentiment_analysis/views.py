from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 

# Create your views here.
def index(request):
    context = {
        'list': [0,1,2,3]
    }
    return render(request, 'sentiment_analysis/index.html', context)
