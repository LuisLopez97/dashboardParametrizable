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
import seaborn as sns
pd.set_option('display.max_colwidth', -1)

class Preprocesamiento:
    diccionario_contracciones = {}
    diccionario_emoticones    = {}
    diccionario_slang         = {}

    def __init__(self, archivo, nombre_columna_texto):
        
        # Lectura de CSV de Tweets
        self.data = pd.read_csv(archivo)

        # Seleccionar la columna con los Tweets
        self.tweets = self.data[nombre_columna_texto]

        # Cargar los diccionarios
        self.diccionario_contracciones = self.loadDiccionarioContracciones()
        self.diccionario_emoticones = self.loadDiccionarioEmoticones()
        #self.diccionario_slang = self.loadDiccionarioSlang()
        
        print(self.tweets.head(20))
        self.limpieza()

    def limpieza(self):
        
        # No URLs
        data_noURL = self.tweets.str.replace('\w+:\/\/\S+', "")
        
        # No Usertags
        data_noUser = data_noURL.str.replace('@(\w+)', "")
        
        # No Hashtags
        data_noHashtag = data_noUser.str.replace('#(\w+)',"")

        # Convertir contracciones
            # Creando un conjunto de contracciones
        conjunto_contracciones = set(self.diccionario_contracciones.keys())

            # Reemplazar apostrofe con comilla simple
        data_noContracciones = data_noHashtag.str.replace("’", "'")

            # Aplicar la funcion traducir_contracciones a cada registro del dataframe
        data_noContracciones = data_noContracciones.apply(
            lambda x: self.traducir_contracciones(x, conjunto_contracciones))


        # Convertir Emoticones
            # Creando un conjunto de emoticones
        conjunto_emoticones = set(self.diccionario_emoticones.keys())
            # Aplicar la funcion traducir_emoticones a cada registro del dataframe
        data_noEmoticones = data_noContracciones.apply(
            lambda x: self.traducir_emoticones(x, conjunto_emoticones))
        
        print(data_noEmoticones.head(20))
    
    def loadDiccionarioContracciones(self):
        return {
            "ain't":"is not",
            "amn't":"am not",
            "aren't":"are not",
            "can't":"cannot",
            "'cause":"because",
            "couldn't":"could not",
            "couldn't've":"could not have",
            "could've":"could have",
            "daren't":"dare not",
            "daresn't":"dare not",
            "dasn't":"dare not",
            "didn't":"did not",
            "doesn't":"does not",
            "don't":"do not",
            "e'er":"ever",
            "em":"them",
            "everyone's":"everyone is",
            "finna":"fixing to",
            "gimme":"give me",
            "gonna":"going to",
            "gon't":"go not",
            "gotta":"got to",
            "hadn't":"had not",
            "hasn't":"has not",
            "haven't":"have not",
            "he'd":"he would",
            "he'll":"he will",
            "he's":"he is",
            "he've":"he have",
            "how'd":"how would",
            "how'll":"how will",
            "how're":"how are",
            "how's":"how is",
            "I'd":"I would",
            "I'll":"I will",
            "I'm":"I am",
            "I'm'a":"I am about to",
            "I'm'o":"I am going to",
            "isn't":"is not",
            "it'd":"it would",
            "it'll":"it will",
            "it's":"it is",
            "I've":"I have",
            "kinda":"kind of",
            "let's":"let us",
            "mayn't":"may not",
            "may've":"may have",
            "mightn't":"might not",
            "might've":"might have",
            "mustn't":"must not",
            "mustn't've":"must not have",
            "must've":"must have",
            "needn't":"need not",
            "ne'er":"never",
            "o'":"of",
            "o'er":"over",
            "ol'":"old",
            "oughtn't":"ought not",
            "shalln't":"shall not",
            "shan't":"shall not",
            "she'd":"she would",
            "she'll":"she will",
            "she's":"she is",
            "shouldn't":"should not",
            "shouldn't've":"should not have",
            "should've":"should have",
            "somebody's":"somebody is",
            "someone's":"someone is",
            "something's":"something is",
            "that'd":"that would",
            "that'll":"that will",
            "that're":"that are",
            "that's":"that is",
            "there'd":"there would",
            "there'll":"there will",
            "there're":"there are",
            "there's":"there is",
            "these're":"these are",
            "they'd":"they would",
            "they'll":"they will",
            "they're":"they are",
            "they've":"they have",
            "this's":"this is",
            "those're":"those are",
            "'tis":"it is",
            "'twas":"it was",
            "wanna":"want to",
            "wasn't":"was not",
            "we'd":"we would",
            "we'd've":"we would have",
            "we'll":"we will",
            "we're":"we are",
            "weren't":"were not",
            "we've":"we have",
            "what'd":"what did",
            "what'll":"what will",
            "what're":"what are",
            "what's":"what is",
            "what've":"what have",
            "when's":"when is",
            "where'd":"where did",
            "where're":"where are",
            "where's":"where is",
            "where've":"where have",
            "which's":"which is",
            "who'd":"who would",
            "who'd've":"who would have",
            "who'll":"who will",
            "who're":"who are",
            "who's":"who is",
            "who've":"who have",
            "why'd":"why did",
            "why're":"why are",
            "why's":"why is",
            "won't":"will not",
            "wouldn't":"would not",
            "would've":"would have",
            "y'all":"you all",
            "you'd":"you would",
            "you'll":"you will",
            "you're":"you are",
            "you've":"you have",
            "Whatcha":"What are you",
            "luv":"love",
            "sux":"sucks",
    }

    def loadDiccionarioEmoticones(self):
        return {
            ":)": "smiley",
            ":‑)": "smiley",
            ":-]": "smiley",
            ":-3": "smiley",
            ":->": "smiley",
            "8-)": "smiley",
            ":-}": "smiley",
            ":)": "smiley",
            ":]": "smiley",
            ":3": "smiley",
            ":>": "smiley",
            "8)": "smiley",
            ":}": "smiley",
            ":o)": "smiley",
            ":c)": "smiley",
            ":^)": "smiley",
            "=]": "smiley",
            "=)": "smiley",
            ":-))": "smiley",
            ":-D": "smiley",
            "8‑D": "smiley",
            "x‑D": "smiley",
            "X‑D": "smiley",
            ":D": "smiley",
            "8D": "smiley",
            "xD": "smiley",
            "XD": "smiley",
            ":-d": "smiley",
            "8‑d": "smiley",
            "x‑d": "smiley",
            "X‑d": "smiley",
            ":d": "smiley",
            "8d": "smiley",
            "xd": "smiley",
            "Xd": "smiley",
            ":‑(": "sad",
            ":‑c": "sad",
            ":‑<": "sad",
            ":‑[": "sad",
            ":(": "sad",
            ":c": "sad",
            ":<": "sad",
            ":[": "sad",
            ":-||": "sad",
            ">:[": "sad",
            ":{": "sad",
            ":@": "sad",
            ">:(": "sad",
            ":'‑(": "sad",
            ":'(": "sad",
            ":‑P": "playful",
            "X‑P": "playful",
            "x‑p": "playful",
            ":‑p": "playful",
            ":‑Þ": "playful",
            ":‑þ": "playful",
            ":‑b": "playful",
            ":P": "playful",
            "XP": "playful",
            "xp": "playful",
            ":p": "playful",
            ":Þ": "playful",
            ":þ": "playful",
            ":b": "playful",
            ";p": "playful",
            "<3": "love",
        }

    def traducir_contracciones(self, texto, contracciones):
        texto = texto.split(" ")
        j = 0
        for palabra in texto:
            # Checa si las palabras seleccionadas coinciden con el connjunto de emoticones
            if palabra in contracciones:
                #print("Contraccion con ", palabra, " a ", diccionario_contracciones[palabra], " en ", texto)
                # Si encuentra una coincidencia, la reemplaza con su respectiva traducción
                texto[j] = self.diccionario_contracciones[palabra]
            j = j + 1
        # Retorna la cadena corregida
        return ' '.join(texto)

    def traducir_emoticones(self, texto, emoticones):
        texto = texto.split(" ")
        j = 0
        for palabra in texto:
            # Checa si las palabras seleccionadas coinciden con el connjunto de emoticones
            if palabra in emoticones:
                # Si encuentra una coincidencia, la reemplaza con su respectiva traducción
                texto[j] = self.diccionario_emoticones[palabra]
            j = j + 1
        # Retorna la cadena corregida
        return ' '.join(texto)

ps = Preprocesamiento("Tweets_pg_prepared.csv", "text")
