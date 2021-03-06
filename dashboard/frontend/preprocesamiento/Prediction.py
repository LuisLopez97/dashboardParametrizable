from .Preprocesamiento import Preprocesamiento as preprocesamiento
from .FeatureExtraction import FeatureExtraction as fe
from pathlib import Path, PurePath
from tqdm import tqdm
import pandas as pd
import numpy as np
import pickle
import os


class Prediction:
    def __init__(self, nombre_clasificador, nombre_vectorizador, test_data, columna_tweets):
        self.nombre_clasificador = nombre_clasificador
        self.nombre_vectorizador = nombre_vectorizador
        self.test_data = test_data
        self.columna_tweets = columna_tweets

    def predecir(self):
        # Definir ruta para lectura de Pickle de clasificador
        ruta_actual = PurePath(Path.cwd()) / 'frontend' / 'preprocesamiento'
        clf = self.loadPickle(ruta_actual, 'Classifiers',
                              self.nombre_clasificador)

        # Definir ruta para lectura de Pickle de vectorizador
        vectorizer = self.loadPickle(
            ruta_actual, 'Vectorizers', self.nombre_vectorizador)

        # Leer dataset real
        dataset = ruta_actual / 'TestData' / self.test_data
        tweets = pd.read_csv(dataset, encoding='ISO-8859-1')
        features = tweets[self.columna_tweets]

        # Preprocesamiento
        prep = preprocesamiento("test.csv", self.columna_tweets, "")
        tweets_limpios = prep.limpieza(features)

        # lemmatización
        print("Iniciar Lemmatización")
        lemmatizated_data = prep.lemmatization(tweets_limpios)

        # Guardar preprocesamiento para el WordCloud
        print("Guardando preprocesamiento para el WordCloud")
        pred_lemmatized = pd.DataFrame({'data_lemmatized': lemmatizated_data})
        archivo = ruta_actual / 'TestData' / 'Output' / 'prediccion_wordcloud.csv'
        pred_lemmatized.to_csv(archivo, index=None, header=True)

        # Feature Extraction: Bag of Words
        print("Feature Extraction: Bag of Words")
        count_test = vectorizer.transform(lemmatizated_data.values.astype('U'))

        # Prediccion
        print("Prediccion con " + self.nombre_clasificador +
              " y vectorizador " + self.nombre_vectorizador)
        pred = clf.predict(count_test)

        # Unir prediccion al Dataframe
        # tweets.insert(0, 'Sentiment', pred)
        tweets['Sentiment'] = pred

        # Convertir numeros a palabras
        tweets["Sentiment"] = tweets["Sentiment"].replace(
            to_replace=[1, 0, -1], value=["positivo", "neutral", "negativo"])

        # Guardar a CSV
        print("Guardando prediccion como CSV...")
        # Ruta actual
        ruta_actual = PurePath(Path.cwd())
        archivo = ruta_actual / 'frontend' / 'preprocesamiento' / \
            'TestData' / 'Output' / 'prediccion.csv'  # Direccion CSV
        tweets.to_csv(archivo, index=None, header=True)

        # Guardar como JSON
        print("Guardando prediccion como JSON...")
        # archivo = ruta_actual.parent.parent / 'frontend' / 'prediccion.json'  # Direccion JSON
        archivo = ruta_actual / 'img' / 'prediccion.json'        # Direccion CSV
        with open(archivo, 'w', encoding='ISO-8859-1') as file:
            tweets.to_json(file, orient='records', force_ascii=False)

    def loadPickle(self, cur_path, carpeta, _pickle):
        _archivo = os.path.join(cur_path, carpeta, _pickle)
        print(f"Abriendo Pickle {_pickle}...")
        with open(_archivo, 'rb') as infile:
            clf = pickle.load(infile)
        print(f"Pickle {_pickle} abierto con exito")
        return clf
