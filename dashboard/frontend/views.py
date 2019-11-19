from django.shortcuts import render
from django.http import HttpResponse
from . import testing
from shutil import copy

import os
import json


def index(request):
    return render(request, 'frontend/index.html')


def test(request):
    if request.method == 'POST':
        if os.path.isfile("img/tweetsp.json"):
            os.remove("img/tweetsp.json")
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        palabra = data.get('keyword')
        print(palabra)
        idioma = data.get('idioma')
        print(idioma)
        copy("tweets3p.json", "img/tweetsp.json")
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=404)
