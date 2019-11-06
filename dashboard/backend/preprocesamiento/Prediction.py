from Preprocesamiento import Preprocesamiento as preprocesamiento
from FeatureExtraction2 import FeatureExtraction as fe
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
        ruta_actual = PurePath(Path.cwd())
        clf = self.loadPickle(ruta_actual, 'Classifiers', self.nombre_clasificador)

        # Definir ruta para lectura de Pickle de vectorizador
        vectorizer = self.loadPickle(ruta_actual, 'Vectorizers', self.nombre_vectorizador)

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
        print("Guardando prediccion como CSV...")
        ruta_actual = PurePath(Path.cwd())                                # Ruta actual
        archivo = ruta_actual / 'TestData' / 'Output' / 'prediccion.csv'  # Direccion CSV
        tweets.to_csv(archivo, index=None, header=True)

        # Guardar como JSON
        print("Guardando prediccion como JSON...")
        archivo = ruta_actual.parent.parent / 'frontend' / 'prediccion.json'  # Direccion JSON
        tweets.to_json(archivo, orient='records', lines=True)

    def loadPickle(self, cur_path, carpeta, _pickle):
        _archivo = os.path.join(cur_path, carpeta, _pickle)
        print(f"Abriendo Pickle {_pickle}...")
        with open(_archivo, 'rb') as infile:
            clf = pickle.load(infile)
        print(f"Pickle {_pickle} abierto con exito")
        return clf
