# Propósito: Recibir un CSV con Tweets y preprocesarlos (limpiarlos) para su futuro tratamiento 
# con alguna herramienta de Feature Extraction
# Creado el 18 de octubre de 2019
# Autor: Alejandro Gibran Pérez Pérez

# Importar de librerías
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import emoji
import json
import seaborn as sns

class Preprocesamiento:
    columna_texto             = ""
    columna_sentimiento       = ""
    diccionario_contracciones = {}
    diccionario_emoticones    = {}
    diccionario_slang         = {}


    def __init__(self, archivo, columna_texto, columna_sentimiento):
        # Actualizar diccionarios
        pd.set_option('display.max_colwidth', -1)
        nltk.download('stopwords')

        # Guardar argumentos para la instancia
        self.columna_texto = columna_texto
        self.columna_sentimiento = columna_sentimiento

        # Lectura de CSV de Tweets
        self.tweets_df = pd.read_csv(archivo)

        # Seleccionar la columna con los Tweets
        self.tweets = self.tweets_df[columna_texto]

        # Cargar los diccionarios
        self.diccionario_contracciones = self.json2dict("contractions.json")    # Contracciones
        self.diccionario_emoticones    = self.json2dict("emoticons.json")       # Emoticones
        self.diccionario_slang         = self.json2dict("slang.json")           # Slang

        # Iniciar Limpieza
        tweets_limpios = self.limpieza()

        # Iniciar lemmatización
        lemmatizated_data = self.lemmatization(tweets_limpios["clean_text"])

        # Borrar la columna de datos limpios
        del tweets_limpios["clean_text"]

        # Añadir columna de datos lemmatizados
        tweets_limpios.insert(0, 'data_lemmatized', lemmatizated_data)

        # Sustitur los valores de la columna de sentimientos por 1, 0 , -1
        tweets_limpios["sentiment"] = tweets_limpios["sentiment"].replace(to_replace=["positive","neutral","negative"], value=[1,0,-1])

        # Guardar el Dataframe como un CSV
        export_csv = tweets_limpios.to_csv (r'data_lemmatized.csv', index = None, header=True)


    def limpieza(self):
        # No URLs
        self.tweets = self.tweets.str.replace('\w+:\/\/\S+', "")

        # No Usertags
        self.tweets = self.tweets.str.replace('@(\w+)', "")
        
        # No Hashtags
        self.tweets = self.tweets.str.replace('#(\w+)',"")

        # Convertir contracciones
        conjunto_contracciones = set(self.diccionario_contracciones.keys())     # Creando un conjunto de contracciones
        self.tweets = self.tweets.str.replace("’", "'")                         # Reemplazar apostrofe con comilla simple
        self.tweets = self.tweets.apply(                                        # Traducir cada registro del dataframe
            lambda x: self.traducir(x, self.diccionario_contracciones, conjunto_contracciones)) 

        # Convertir Emoticones
        conjunto_emoticones = set(self.diccionario_emoticones.keys())           # Creando un conjunto de emoticones            
        self.tweets = self.tweets.apply(                                        # Traducir cada registro del dataframe
            lambda x: self.traducir(x, self.diccionario_emoticones, conjunto_emoticones))
        
        # Convertir emoticones
        self.tweets = self.tweets.apply(lambda x: emoji.demojize(x))
        self.tweets = self.tweets.str.replace(":"," ")

        # Remover signos de puntuación
        self.tweets = self.tweets.str.replace("[\.\,\!\?\:\;\-\=]", " ")
        self.tweets = self.tweets.str.replace(" +"," ")                         # Reducir los espacios a solo 1

        # Convertir todo a minúsculas
        self.tweets = self.tweets.str.lower()

        # Interpretar el slang
        conjunto_slang = set(self.diccionario_slang.keys())                     # Creando un conjunto de slang            
        self.tweets = self.tweets.apply(                                        # Traducir cada registro del dataframe
            lambda x: self.traducir(x, self.diccionario_slang, conjunto_slang))

        # Remover carácteres repetidos
        self.tweets = self.tweets.transform(lambda x: re.sub(r'(.)\1+', r'\1\1', x))

        # Remover StopWords
        stop = stopwords.words("english")
        stop_set = set(stop)
        self.tweets = self.tweets.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_set)]))

        # Unir columna limpia al Dataframe
        return pd.DataFrame(dict(clean_text = self.tweets , sentiment = self.tweets_df[self.columna_sentimiento]))


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
        porter_stemmer_tokenized = texto.apply(lambda x: self.stemOracion(x, ps))
        return porter_stemmer_tokenized

    # Lancaster
    def lancasterStemmer(self, texto):
        nltk.download('punkt')
        ls = LancasterStemmer()
        lancaster_stemmer_tokenized = texto.apply(lambda x: self.stemOracion(x, ls))
        return lancaster_stemmer_tokenized
    

    # Funcion para Lemmatizar
    def lemmatization(self, texto):
        nltk.download('wordnet')
        lm = WordNetLemmatizer()
        data_lemmatized = texto.apply(lambda x: self.stemOracion(x, lm))
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

#Preprocesamiento("Tweets_pg_prepared.csv", "text", "airline_sentiment")