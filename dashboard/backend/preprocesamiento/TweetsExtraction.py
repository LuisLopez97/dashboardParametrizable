#Librerias
from tweepy.streaming import StreamListener
from tweepy import Stream
from pathlib import Path, PurePath
from time import time
from time import sleep
import tweepy
import sys
import os
import csv
import json

#####################################
#Autentificación para acceder a Twitter
#Por medio de las credenciales
class TweepyExtraction:
    
    def __init__(self, tiempo):
        self.tiempo = tiempo
        consumer_key = "hzv8CF7qvlGXvelOOIDOLXvyS" 
        consumer_secret= "WxSn72jW90sP4FL9MEIKPmdbZi8WaPSRwOyN9TwLiE1lrYcecJ" 
        access_token = "1166089196215422976-FBSUbTOiTBqXzFH9frP827kfDksGZy"
        access_token_secret = "Jrce99HJeSxA6Mh9sjRTbb8XsuKrOshdMMCrGYyeGwE9F"
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
        ruta_actual = PurePath(Path.cwd())
        self.ruta_extraccion =  Path(ruta_actual / 'TestData' / 'extraccion_tweets.csv')

    def recoleccion(self, idioma, palabra):
        # Borrar archivo para que se vuelva a escribir
        if self.ruta_extraccion.exists():
            os.remove(self.ruta_extraccion)
        # Inicia recoleccion con idioma seleccionado por usuario
        csvFile = open(self.ruta_extraccion, 'a', encoding='utf-8', newline='')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['Author', 'Date', 'Text'])
        csvFile.close()

        streamingAPI = tweepy.streaming.Stream(self.auth, CustomStreamListener(self.api, self.tiempo))
        if idioma != "en" and idioma != "es":
            print("Idioma no reconocido: " + idioma)
            return
        streamingAPI.filter(languages=[idioma], track=[palabra], is_async=True)
        sleep(self.tiempo)


######################################
#Recolector y escuchador
class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api, tiempo_limite):
        self.api = api
        self.tiempo_limite = tiempo_limite
        self.ruta_actual = PurePath(Path.cwd())
        self.ruta_extraccion =  Path(self.ruta_actual / 'TestData' / 'extraccion_tweets.csv')
        self.tiempo_inicio = time()

    def on_status(self, status):
        tiempo_transcurrido = round(time() - self.tiempo_inicio, 3)
        print("\nTIEMPO TRANSCURRIDO: " + str(tiempo_transcurrido) + "s\n")
        if tiempo_transcurrido > self.tiempo_limite:
            print("I'M ABOUT TO END THIS MAN WHOLE CAREER")
            return False

        text = ""
        if hasattr(status, "retweeted_status"):
            if hasattr(status.retweeted_status, "extended_tweet"):
                text = status.retweeted_status.extended_tweet["full_text"]
            else:
                text = status.retweeted_status.text
        elif hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text
                
        with open(self.ruta_extraccion, 'a', encoding='utf-8', newline='') as f: 
            print(status.author.screen_name, status.created_at, text)
            writer = csv.writer(f)
            writer.writerow([status.author.screen_name, status.created_at, text])


    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True # Don't kill the stream
######################################
