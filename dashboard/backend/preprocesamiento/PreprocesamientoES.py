# Importar de librerías
from LongFunctionProgress import provide_progress_bar
from LongFunctionProgress import progress_wrapped
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from pathlib import Path, PurePath
from tqdm import tqdm
import spacy
import pandas as pd
import numpy as np
import nltk
import emoji
import json
import re
import os

class Preprocesamiento:
    columna_texto             = ""
    columna_sentimiento       = ""
    diccionario_contracciones = {}
    diccionario_emoticones    = {}
    diccionario_slang         = {}


    def __init__(self, archivo, columna_texto, columna_sentimiento):
        self.archivo = archivo
        self.columna_texto = columna_texto
        self.columna_sentimiento = columna_sentimiento

        pd.set_option('display.max_colwidth', -1)
        # Actualizar diccionarios
        print("Actualizando Diccionario: StopWords")
        nltk.download('stopwords')

    def preparacion(self):
        print("===PREPROCESAMIENTO INICIADO===")
        # Lectura de CSV
        ruta_actual = PurePath(Path.cwd())

        # Direccion CSV a preprocesar
        _archivo = ruta_actual / 'DB' / self.archivo

        # Lectura de CSV de Tweets
        print("Lectura de CSV...")
        self.tweets_df = pd.read_csv(_archivo, encoding='ISO-8859-1')

        # Seleccionar la columna con los Tweets
        self.tweets = self.tweets_df[self.columna_texto]

        # Iniciar Limpieza
        print("Iniciar Limpieza")
        tweets = self.limpieza(self.tweets)
        tweets_limpios = pd.DataFrame(
            dict(clean_text=tweets,
                 sentiment=self.tweets_df[self.columna_sentimiento]))

        # Seleccionando solo los Tweets con valor Positivo, Negativo y Neutro
        tweets_limpios = tweets_limpios.loc[tweets_limpios['sentiment'] != "NONE"]

        # Sustitur los valores de la columna de sentimientos por 1, 0 , -1
        tweets_limpios["sentiment"] = tweets_limpios["sentiment"].replace(to_replace=["P", "NEU", "N"], value=[1, 0, -1])

        # Iniciar lemmatización
        print("Iniciar Lemmatización")
        lemmatizated_data = self.lemmatizacion(tweets_limpios["clean_text"])

        # Borrar la columna de datos limpios
        del tweets_limpios["clean_text"]

        # Añadir columna de datos lemmatizados
        tweets_limpios.insert(0, 'data_lemmatized', lemmatizated_data)

        # Guardar el Dataframe como un CSV
        print("Guardando Tweets Limpios a CSV...")
        # Ruta actual
        ruta_actual = PurePath(Path.cwd())
        # Direccion CSV data_lemmatized.csv
        archivo = ruta_actual / 'DB' / 'data_lemmatized_es.csv'
        tweets_limpios.to_csv(archivo, index=None, header=True)
        print("===PREPROCESAMIENTO TERMINADO===")

    def limpieza(self, tweets):
        # No URLs
        print("No URLs")
        tweets = tweets.str.replace(r'\w+:\/\/\S+', "")

        # No Usertags
        print("No Usertags")
        tweets = tweets.str.replace(r'@(\w+)', "")

        # No Hashtags
        print("No Hashtags")
        tweets = tweets.str.replace(r'#(\w+)',"")

        # Remover Emoticones
        print("Convertir Emoticones")
        tweets = tweets.str.replace("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001f926-\U0001f937"
                        u'\U00010000-\U0010ffff'
                        u"\u200d"
                        u"\u2640-\u2642"
                        u"\u2600-\u2B55"
                        u"\u23cf"
                        u"\u23e9"
                        u"\u231a"
                        u"\u3030"
                        u"\ufe0f"
            "]+", "")


        # Convertir todo a minúsculas
        print("Convertir todo a minúsculas")
        tweets = tweets.str.lower()

        # Remover todo lo que no sea letras para este punto
        print("Remover todo lo que no sea letras para este punto")
        tweets = tweets.str.replace(r'[^a-zA-Z ]+', '')

        # Remover carácteres repetidos
        print("Remover carácteres repetidos")
        tweets = tweets.transform(lambda x: re.sub(r'(.)\1+', r'\1\1', str(x)))

        # Remover StopWords
        print("Remover StopWords")
        stop = stopwords.words("spanish")
        stop_set = set(stop)
        stop_set.discard('no')
        tweets = tweets.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_set)]))

        # Unir columna limpia al Dataframe
        return tweets


    # Funcion para Lemmatizar
    @progress_wrapped(estimated_time=100)
    def lemmatizacion(self, texto):
        print("Lemmatización...")
        nlp = spacy.load('es')
        data_Lemmatizer = texto.apply(lambda x: self.lematizarOracion(x, nlp))
        print("===LEMMATIZACIÓN TERMINADA===")
        return data_Lemmatizer

    def lematizarOracion(self,tweet, nlp):
        resultado = []
        for token in nlp(tweet):
            resultado.append(token.lemma_)
        return " ".join(resultado)

# Preprocesamiento("Tweets_pg_prepared.csv", "text", "airline_sentiment")
