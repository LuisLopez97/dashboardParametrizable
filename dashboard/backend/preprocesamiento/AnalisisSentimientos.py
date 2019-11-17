from TweetsExtraction import TweepyExtraction as tweepy_extraction
from Preprocesamiento import Preprocesamiento as preprocesamiento_en
from PreprocesamientoES import Preprocesamiento as preprocesamiento_es
from FeatureExtraction import FeatureExtraction as feature_extraction
from Prediction import Prediction as prediction
from pathlib import Path, PurePath
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import sys
from time import time

def instalarLibrarias():
    # Instala las librerías necesarias para ejecutar el proceso de modelado
    subprocess.call([sys.executable, "-m", "pip", "install","-r", "requirements.txt"])

def extraccion(idioma, palabra, tiempo):
    print("=== RECOLECCION INICIADA ===")
    # Inicializando objeto TweepyExtraction
    ext = tweepy_extraction(tiempo)
    # Ejecutando recoleccion
    ext.recoleccion(idioma, palabra)

def entrenar(dataset_entrenamiento, columna_tweets, columna_sentimientos, idioma):
    if idioma == "en":
        # Inicializando clase preprocesamiento en ingles
        prep = preprocesamiento_en(dataset_entrenamiento, columna_tweets, columna_sentimientos)
        # Iniciando Contador de tiempo para preparacion
        t0 = time()
        # Ejecutando la preparación de los datos
        prep.preparacion()
        # Imprimir el tiempo de ejecución
        print("TIEMPO PREPARACION DATOS INGLES: ", round(time() - t0, 3), "s")
        # Iniciando Contador de tiempo
        t0 = time()
        print("=== ENTRENAMIENTO INICIADO ===")
        # Inicializando la clase feature_extraction
        fe = feature_extraction("data_lemmatized.csv",
                                'data_lemmatized', "sentiment", "en")
        # Ejecutando la extracción, indicandole el tipo de extraccion
        fe.extraction('bagofwords')
        print("=== ENTRENAMIENTO TERMINADO EXITOSAMENTE ===")
        # Imprimir el tiempo de ejecución
        print("TIEMPO ENTRENAMIENTO: ", round(time() - t0, 3), "s")
    elif idioma == "es":
        # # Inicializando clase preprocesamiento en español
        # prep = preprocesamiento_es(dataset_entrenamiento, columna_tweets, columna_sentimientos)
        # # Iniciando Contador de tiempo para preparacion
        # t0 = time()
        # # Ejecutando la preparación de los datos
        # prep.preparacion()
        # # Imprimir el tiempo de ejecución
        # print("TIEMPO PREPARACION DATOS ESPAÑOL: ", round(time() - t0, 3), "s")
        # Iniciando Contador de tiempo
        t0 = time()
        print("=== ENTRENAMIENTO INICIADO ===")
        # Inicializando la clase feature_extraction
        fe = feature_extraction("data_lemmatized_es.csv",
                                'data_lemmatized', "sentiment", "es")
        # Ejecutando la extracción, indicandole el tipo de extraccion
        fe.extraction('bagofwords')
        print("=== ENTRENAMIENTO TERMINADO EXITOSAMENTE ===")
        # Imprimir el tiempo de ejecución
        print("TIEMPO ENTRENAMIENTO: ", round(time() - t0, 3), "s")
    else: 
        print("Ningun idioma seleccionado, terminando.")
        return

def predecir(dataset, columna_tweets, idioma):
    if idioma == "en":
        # Inicializando clase prediction
        pred = prediction("LogisticRegression_en", 'CountVectorizer_en', dataset, columna_tweets)
    elif idioma == "es":
        # Inicializando clase prediction
        pred = prediction("LogisticRegression_es", 'CountVectorizer_es', dataset, columna_tweets)
    else: 
        print("Idioma no reconocido. Terminano.")
        return
    # Iniciando Contador de tiempo
    t0 = time()
    # Ejecutando la predicción
    pred.predecir()
    # Imprimir el tiempo de ejecución
    print("TIEMPO PREDICCIÓN: ", round(time() - t0, 3), "s")

def wordcloud(nombre_wordcloud, color_fondo):
    print("=== WORDCLOUD INICIADO ===")
    # Definir ruta actual
    ruta_actual = PurePath(Path.cwd())
    archivo = ruta_actual / 'TestData' / 'Output' / 'prediccion.csv'
    # Leer Predicción
    print("Lectura de Datasets")
    pred_df = pd.read_csv(archivo, encoding='ISO-8859-1')
    # Leer Extracción Lematizada
    archivo = ruta_actual / 'TestData' / 'Output' / 'prediccion_wordcloud.csv'
    pred_wordcloud_df = pd.read_csv(archivo, encoding='ISO-8859-1')
    # Crearle la columna "sentimiento" al CSV de Extracción
    pred_wordcloud_df["sentiment"] = pred_df["Sentiment"]
    # Filtrar tweets por sentimiento
    pred_pos = pred_wordcloud_df[pred_df['Sentiment'] == 'positivo']
    pred_neg = pred_wordcloud_df[pred_df['Sentiment'] == 'negativo']
    pred_neu = pred_wordcloud_df[pred_df['Sentiment'] == 'neutral']

    # Creando WordClouds
    def crearWordCloud(dataframe, sentimiento):
        # Unificar todos los textos de todas las columnas del dataframe en uno
        text = dataframe.data_lemmatized.values
        # Creando el WordCloud General
        print("Creando el WordCloud ", sentimiento)
        wordcloud = WordCloud(
            width=1024, height=720, background_color=color_fondo, collocations=False).generate(str(text))
        print("Guardando WordCloud: wordcloud_" + nombre_wordcloud + ".png")
        # Creando carpeta de WordCloud especifico
        carpeta = Path(ruta_actual / 'TestData' / 'Output' / 'WordCloud' / nombre_wordcloud)
        if not carpeta.exists():
            carpeta.mkdir(exist_ok=True)
            print("Directorio: ", carpeta,  " creado")
        else:
            print("Directorio:  ", carpeta,  " ya existe")
        archivo = Path(ruta_actual / 'TestData' / 'Output' / 'WordCloud' / nombre_wordcloud / (
            "wordcloud_" + nombre_wordcloud + "_" + sentimiento + "_" + color_fondo + ".png"))
        wordcloud.to_file(archivo)

    crearWordCloud(pred_wordcloud_df, "general")
    crearWordCloud(pred_pos, "positivo")
    crearWordCloud(pred_neg, "negativo")
    crearWordCloud(pred_neu, "neutral")

    
