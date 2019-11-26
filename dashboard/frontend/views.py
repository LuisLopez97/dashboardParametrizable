import os
import json
import datetime as dt

from django.shortcuts import render
from django.http import HttpResponse
from shutil import copy
from .preprocesamiento import AnalisisSentimientos as sentimiento


def index(request):
    return render(request, 'frontend/index.html')


def test(request):
    if request.method == 'POST':
        if os.path.isfile("img/prediccion.json"):
            os.remove("img/prediccion.json")
        data = json.loads(request.body.decode('utf-8'))
        palabra = data.get('keyword')
        idioma = data.get('idioma')
        tweets = int(data.get('tweets'))
        fecha_inicio = dt.date.today() - dt.timedelta(days=15)
        """ extraccionHistorico(palabra, idioma, limite_tweets, fecha_inicio, fecha_final, bins) """
        sentimiento.extraccionHistorico(
            palabra,  idioma, tweets, fecha_inicio)
        sentimiento.predecir("extraccion_tweets.csv", "Text", idioma)
        sentimiento.wordcloud(palabra, "white", idioma)
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=404)
