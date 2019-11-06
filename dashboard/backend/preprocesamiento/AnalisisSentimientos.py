from Preprocesamiento import Preprocesamiento as preprocesamiento
from FeatureExtraction2 import FeatureExtraction as feature_extraction
from Prediction import Prediction as prediction
import pandas as pd
import subprocess
import sys

def importarLibrarias():
    subprocess.call([sys.executable, "-m", "pip", "install","-r", "requirements.txt"])


def entrenar(dataset_entrenamiento, columna_tweets, columna_sentimientos):
    #prep = preprocesamiento(dataset_entrenamiento, columna_tweets, columna_sentimientos)
    #prep.preparacion()
    print("=== ENTRENAMIENTO INICIADO ===")
    fe = feature_extraction("data_lemmatized.csv", 'data_lemmatized', "sentiment")
    fe.extraction('tfidf')
    print("=== ENTRENAMIENTO TERMINADO EXITOSAMENTE ===")


def predecir(dataset, columna_tweets):
    pred = prediction("MultinomialNB", 'CountVectorizer', dataset, columna_tweets)
    pred.predecir()