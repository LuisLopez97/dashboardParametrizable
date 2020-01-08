# Propósito: Recibir un CSV con Tweets y preprocesarlos (limpiarlos) para su futuro tratamiento
# con alguna herramienta de Feature Extraction
# Creado el 18 de octubre de 2019
# Autor: Alejandro Gibran Pérez Pérez

# Importar de librerías
from .longFunctionProgress import provide_progress_bar
from .longFunctionProgress import progress_wrapped
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from pathlib import Path, PurePath
from tqdm import tqdm
import pandas as pd
import numpy as np
import nltk
import emoji
import json
import re
import os


class Preprocesamiento:
    columna_texto = ""
    columna_sentimiento = ""
    diccionario_contracciones = {}
    diccionario_emoticones = {}
    diccionario_slang = {}

    def __init__(self, archivo, columna_texto, columna_sentimiento):
        self.archivo = archivo
        self.columna_texto = columna_texto
        self.columna_sentimiento = columna_sentimiento

        pd.set_option('display.max_colwidth', -1)
        # Actualizar diccionarios
        # print("Actualizando Diccionario: StopWords")
        # nltk.download('punkt')
        # nltk.download('wordnet')
        nltk.download('stopwords')

        # Cargar los diccionarios
        print("Cargando Diccionarios...")
        # Ruta actual
        ruta_actual = PurePath(Path.cwd())
        # Direccion diccionario contractions.json
        diccionario = ruta_actual / 'frontend' / \
            'preprocesamiento' / 'DB' / 'contractions.json'
        self.diccionario_contracciones = self.json2dict(
            diccionario)    # Contracciones
        # Direccion diccionario emoticons.json
        diccionario = ruta_actual / 'frontend' / \
            'preprocesamiento' / 'DB' / 'emoticons.json'
        self.diccionario_emoticones = self.json2dict(
            diccionario)       # Emoticones
        # Direccion diccionario emoticons.json
        diccionario = ruta_actual / 'frontend' / \
            'preprocesamiento' / 'DB' / 'slang.json'
        self.diccionario_slang = self.json2dict(diccionario)            # Slang
        print("Diccionarios cargados exitosamente")

    def preparacion(self):
        print("===PREPROCESAMIENTO INICIADO===")

        # Lectura de CSV
        self.path('DB')

        # Iniciar Limpieza
        print("Iniciar Limpieza")
        tweets = self.limpieza(self.tweets)
        tweets_limpios = pd.DataFrame(
            dict(clean_text=tweets,
                 sentiment=self.tweets_df[self.columna_sentimiento]))

        # Iniciar lemmatización
        print("Iniciar Lemmatización")
        lemmatizated_data = self.porterStemmer(tweets_limpios["clean_text"])

        # Borrar la columna de datos limpios
        del tweets_limpios["clean_text"]

        # Añadir columna de datos lemmatizados
        tweets_limpios.insert(0, 'data_lemmatized', lemmatizated_data)

        # Sustitur los valores de la columna de sentimientos por 1, 0 , -1
        tweets_limpios["sentiment"] = tweets_limpios["sentiment"].replace(
            to_replace=["positive", "neutral", "negative"], value=[1, 0, -1])

        # Guardar el Dataframe como un CSV
        print("Guardando Tweets Limpios a CSV...")
        # Ruta actual
        ruta_actual = PurePath(Path.cwd())
        # Direccion CSV data_lemmatized.csv
        archivo = ruta_actual / 'frontend' / \
            'preprocesamiento' / 'DB' / 'data_lemmatized.csv'
        tweets_limpios.to_csv(archivo, index=None, header=True)
        print("===PREPROCESAMIENTO TERMINADO===")

    def path(self, carpeta):

        # Cargando rutas
        # Ruta actual
        ruta_actual = PurePath(Path.cwd())
        # Direccion CSV a preprocesar
        _archivo = ruta_actual / 'frontend' / 'preprocesamiento' / carpeta / self.archivo

        # Lectura de CSV de Tweets
        print("Lectura de CSV...")
        self.tweets_df = pd.read_csv(_archivo)

        # Seleccionar la columna con los Tweets
        self.tweets = self.tweets_df[self.columna_texto]

    def limpieza(self, tweets):
        # No URLs
        print("No URLs")
        tweets = tweets.str.replace('\w+:\/\/\S+', "")

        # No Usertags
        print("No Usertags")
        tweets = tweets.str.replace('@(\w+)', "")

        # No Hashtags
        print("No Hashtags")
        tweets = tweets.str.replace('#(\w+)', "")

        # Convertir contracciones
        print("Convertir contracciones")
        # Creando un conjunto de contracciones
        conjunto_contracciones = set(self.diccionario_contracciones.keys())
        # Reemplazar apostrofe con comilla simple
        tweets = tweets.str.replace("’", "'")
        tweets = tweets.apply(                                        # Traducir cada registro del dataframe
            lambda x: self.traducir(x, self.diccionario_contracciones, conjunto_contracciones))

        # Convertir Emoticones
        print("Convertir Emoticones")
        # Creando un conjunto de emoticones
        conjunto_emoticones = set(self.diccionario_emoticones.keys())
        tweets = tweets.apply(                                        # Traducir cada registro del dataframe
            lambda x: self.traducir(x, self.diccionario_emoticones, conjunto_emoticones))

        # Convertir emojis
        print("Convertir emojis")
        tqdm.pandas(desc="my bar!")
        tweets = tweets.progress_apply(lambda x: emoji.demojize(x))
        tweets = tweets.str.replace(":", " ")

        # Remover todo menos letras y numeros (y espacios)
        print("Remover todo menos letras y numeros (y espacios)")
        tweets = tweets.str.replace('[^0-9a-zA-Z ]+', '')
        # Reducir los espacios a solo 1
        tweets = tweets.str.replace(" +", " ")

        # Convertir todo a minúsculas
        print("Convertir todo a minúsculas")
        tweets = tweets.str.lower()

        # Interpretar el slang
        print("Interpretar el slang")
        # Creando un conjunto de slang
        conjunto_slang = set(self.diccionario_slang.keys())
        tweets = tweets.apply(                                        # Traducir cada registro del dataframe
            lambda x: self.traducir(x, self.diccionario_slang, conjunto_slang))

        # Remover todo lo que no sea letras para este punto
        print("Remover todo lo que no sea letras para este punto")
        tweets = tweets.str.replace('[^a-zA-Z ]+', '')

        # Remover carácteres repetidos
        print("Remover carácteres repetidos")
        tweets = tweets.transform(lambda x: re.sub(r'(.)\1+', r'\1\1', x))

        # Remover StopWords
        # print("Remover StopWords")
        # stop = stopwords.words("english")
        # stop_set = set(stop)
        # tweets = tweets.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_set)]))

        # Unir columna limpia al Dataframe
        return tweets

    # Funcion para traducir palabras de un texto por su respectivo significado

    def traducir(self, texto, diccionario, conjunto):
        texto = texto.split(" ")
        j = 0
        for palabra in texto:
            if diccionario == self.diccionario_slang:
                palabra = palabra.upper()
            # Checa si las palabras seleccionadas coinciden con el connjunto de emoticones
            if palabra in conjunto:
                #print("Contraccion con ", palabra, " a ", diccionario_contracciones[palabra], " en ", texto)
                # Si encuentra una coincidencia, la reemplaza con su respectiva traducción
                texto[j] = diccionario[palabra]
            j = j + 1
        # Retorna la cadena corregida
        return ' '.join(texto)

    # Funcion para convertir un archivo JSON a diccionario

    def json2dict(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
        return dictionary

    # Funcion para Stemmizar
    # Porter

    def porterStemmer(self, texto):
        nltk.download('punkt')
        ps = PorterStemmer()
        porter_stemmer_tokenized = texto.apply(
            lambda x: self.stemOracion(x, ps))
        return porter_stemmer_tokenized

    # Lancaster
    def lancasterStemmer(self, texto):
        nltk.download('punkt')
        ls = LancasterStemmer()
        lancaster_stemmer_tokenized = texto.apply(
            lambda x: self.stemOracion(x, ls))
        return lancaster_stemmer_tokenized

    @progress_wrapped(estimated_time=100)
    # Funcion para Lemmatizar
    def lemmatization(self, texto):
        print("Actualizando Diccionario: Lemmatizacion")
        # nltk.download('wordnet')
        lm = WordNetLemmatizer()
        print("Lemmatización...")
        data_lemmatized = texto.apply(lambda x: self.stemOracion(x, lm))
        print("===LEMMATIZACIÓN TERMINADA===")
        return data_lemmatized

    # Funcion que Tokeniza y realiza el stemmizacion o la lemmatizacion

    def stemOracion(self, oracion, stemmer):
        token_words = word_tokenize(oracion)
        resultado = []
        lemmatizer = False
        if "lemmatize" in dir(stemmer):
            lemmatizer = True
        for word in token_words:
            if lemmatizer:
                resultado.append(stemmer.lemmatize(word, pos="v"))
            else:
                resultado.append(stemmer.stem(word))
        return " ".join(resultado)

    # Funcion para hacer POS tag

    def posTag(self, texto):
        nltk.download('averaged_perceptron_tagger')
        data_POS = texto.apply(lambda x: nltk.pos_tag(nltk.word_tokenize(x)))
        return data_POS

# Preprocesamiento("Tweets_pg_prepared.csv", "text", "airline_sentiment")
