
#Librerias
from tweepy.streaming import StreamListener
from tweepy import Stream
from pathlib import Path, PurePath
from time import sleep
from time import time
import datetime as dt
import pandas as pd
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

class ScrappingExtraction:
    def __init__(self, palabra, limite=None, fecha_inicio=dt.date(2019, 10, 1), fecha_final=dt.date.today(), idioma='en', bins=20):
        self.palabra = palabra
        self.limite = limite
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.idioma = idioma
        self.bins = bins
        self.ruta_extraccion = Path(PurePath(Path.cwd()) / 'TestData' / 'extraccion_tweets.csv')

    def recoleccion(self):
        from twitterscraper import query_tweets
        # Inicia recoleccion con idioma seleccionado por usuario
        print("=== RECOLECCIÓN TWEETSCRAPPING INICIADO")
        list_of_tweets = query_tweets(
            query = self.palabra, 
            limit = self.limite, 
            begindate = self.fecha_inicio, 
            enddate = self.fecha_final, 
            lang = self.idioma, 
            poolsize = self.bins
            )
        # Transforma recolección a lista de diccionarios
        print("Transformando recolección a diccionarios...")
        tweets = self.get_tweets_info(list_of_tweets)
        # Crear Dataframe
        dataframe = pd.DataFrame(tweets)
        # Filtrar por columnas de interes
        tweets_df = dataframe[["username", "timestamp", "text"]]
        # Estandarizar nombre de las columnas
        tweets_df = tweets_df.rename(columns={"username": "Author", "timestamp": "Date", "text": "Text"})
        # Borrar archivo para que se vuelva a escribir
        if self.ruta_extraccion.exists():
            os.remove(self.ruta_extraccion)
        # Exportar extracción a CSV
        print("Exportando CSV: extraccion_tweets.csv")
        tweets_df.to_csv(self.ruta_extraccion, index=None, header=True)

    def get_tweets_info(self, list_of_tweets):
        list_of_tweets_final = []
        twitter_data = {}
        for tweets in list_of_tweets:
            twitter_data = {
                "screen_name": tweets.screen_name,
                "username": tweets.username,
                "user_id": tweets.user_id,
                "tweet_id": tweets.tweet_id,
                "tweet_url": tweets.tweet_url,
                "timestamp": tweets.timestamp,
                "timestamp_epochs": tweets.timestamp_epochs,
                "text": tweets.text,
                "text_html": tweets.text_html,
                "links": tweets.links,
                "hashtags": tweets.hashtags,
                "has_media": tweets.has_media,
                "img_urls": tweets.img_urls,
                "video_url": tweets.video_url,
                "likes": tweets.likes,
                "retweets": tweets.retweets,
                "replies": tweets.replies,
                "is_replied": tweets.is_replied,
                "is_reply_to": tweets.is_reply_to,
                "parent_tweet_id": tweets.parent_tweet_id,
                "reply_to_users": tweets.reply_to_users
            }
            list_of_tweets_final.append(twitter_data)
        return list_of_tweets_final
    
    
