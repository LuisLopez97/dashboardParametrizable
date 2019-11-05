from Preprocesamiento import Preprocesamiento as preprocesamiento
from FeatureExtraction2 import FeatureExtraction as fe
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
        cur_path = os.path.dirname(__file__)
        clf = self.loadPickle(cur_path, 'Classifiers', self.nombre_clasificador)

        # Definir ruta para lectura de Pickle de vectorizador
        cur_path = os.path.dirname(__file__)
        vectorizer = self.loadPickle(cur_path, 'Vectorizers', self.nombre_vectorizador)

        # Leer dataset real
        dataset = os.path.join(cur_path, 'TestData', self.test_data)
        tweets = pd.read_csv(dataset, encoding='ISO-8859-1')
        features = tweets[self.columna_tweets]

        # Preprocesamiento
        prep = preprocesamiento("test.csv", self.columna_tweets, "")
        tweets_limpios = prep.limpieza(features)

        # lemmatización
        print("Iniciar Lemmatización")
        lemmatizated_data = prep.lemmatization(tweets_limpios)

        # Feature Extraction: Bag of Words
        print("Feature Extraction: Bag of Words")
        count_test = vectorizer.transform(lemmatizated_data.values.astype('U'))

        # Prediccion
        print("Prediccion con Multinomial Naive Bayes")
        pred = clf.predict(count_test)

        # Unir prediccion al Dataframe
        # tweets.insert(0, 'sentiment', pred)
        tweets['sentiment'] = pred

        # Guardar a CSV
        cur_path = os.path.dirname(__file__)
        print("Guardando prediccion a CSV...")
        archivo = os.path.join(cur_path, 'TestData', 'Output', 'prediccion.csv')
        tweets.to_csv(archivo, index=None, header=True)

        # Guardar como JSON
        print("Guardando prediccion a JSON...")
        archivo = os.path.join(cur_path, 'TestData', 'Output','prediccion.json')
        tweets.to_json(archivo, orient='records', lines=True)

    def loadPickle(self, cur_path, carpeta, _pickle):
        _archivo = os.path.join(cur_path, carpeta, _pickle)
        print(f"Abriendo Pickle {_pickle}...")
        with open(_archivo, 'rb') as infile:
            clf = pickle.load(infile)
        print(f"Pickle {_pickle} abierto con exito")
        return clf
