from Preprocesamiento import Preprocesamiento as preprocesamiento
from FeatureExtraction import FeatureExtraction as feature_extraction
from Prediction import Prediction as prediction
import pandas as pd
import subprocess
import sys
from time import time

def instalarLibrarias():
    # Instala las librerías necesarias para ejecutar el proceso de modelado
    subprocess.call([sys.executable, "-m", "pip", "install","-r", "requirements.txt"])


def entrenar(dataset_entrenamiento, columna_tweets, columna_sentimientos):
    # Inicializando clase preprocesamiento
    # prep = preprocesamiento(dataset_entrenamiento, columna_tweets, columna_sentimientos)
    # Iniciando Contador de tiempo para preparacion
    # t0 = time()
    # Ejecutando la preparación de los datos
    # prep.preparacion()
    # Imprimir el tiempo de ejecución
    # print("TIEMPO PREPARACION DATOS: ", round(time() - t0, 3), "s")
    # Iniciando Contador de tiempo
    t0 = time()
    print("=== ENTRENAMIENTO INICIADO ===")
    # Inicializando la clase feature_extraction
    fe = feature_extraction("data_lemmatized_es.csv", 'data_lemmatized', "sentiment")
    # Ejecutando la extracción, indicandole el tipo de extraccion
    fe.extraction('bagofwords')
    print("=== ENTRENAMIENTO TERMINADO EXITOSAMENTE ===")
    # Imprimir el tiempo de ejecución
    print("TIEMPO ENTRENAMIENTO: ", round(time() - t0, 3), "s")


def predecir(dataset, columna_tweets):
    # Inicializando clase prediction
    pred = prediction("SGD", 'CountVectorizer', dataset, columna_tweets)
    # Iniciando Contador de tiempo
    t0 = time()
    # Ejecutando la predicción
    pred.predecir()
    # Imprimir el tiempo de ejecución
    print("TIEMPO PREDICCIÓN: ", round(time() - t0, 3), "s")
