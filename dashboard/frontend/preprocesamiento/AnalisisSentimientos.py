from .TweetsExtraction import TweepyExtraction as tweepy_extraction
from .TweetsExtraction import ScrappingExtraction as scrapping_extraction
from .Preprocesamiento import Preprocesamiento as preprocesamiento_en
from .PreprocesamientoES import Preprocesamiento as preprocesamiento_es
from .FeatureExtraction import FeatureExtraction as feature_extraction
from .Prediction import Prediction as prediction
from pathlib import Path, PurePath
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from PIL import Image
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import subprocess
import sys
from time import time


def instalarLibrarias(ruta_archivo):
    # Instala las librerías necesarias para ejecutar el proceso de modelado
    subprocess.call([sys.executable, "-m", "pip",
                     "install", "-r", ruta_archivo])


def extraccionTiempoReal(palabra, idioma, tiempo):
    print("=== RECOLECCION INICIADA ===")
    # Inicializando objeto TweepyExtraction
    ext = tweepy_extraction(tiempo)
    # Ejecutando recoleccion
    ext.recoleccion(idioma, palabra)


def extraccionHistorico(palabra, idioma='en', limite_tweets=None, fecha_inicio=dt.date(2019, 10, 1), fecha_final=dt.date.today(), bins=20):
    # Validación de idioma
    if idioma != "en" and idioma != "es":
        print("Idioma no reconocido: " + idioma)
        return
    # Inicializando objeto TweepyExtraction
    ext = scrapping_extraction(
        palabra, limite_tweets, fecha_inicio, fecha_final, idioma, bins)
    # Ejecutando recoleccion
    ext.recoleccion()


def entrenar(dataset_entrenamiento, columna_tweets, columna_sentimientos, idioma):
    if idioma == "en":
        # Inicializando clase preprocesamiento en ingles
        prep = preprocesamiento_en(
            dataset_entrenamiento, columna_tweets, columna_sentimientos)
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
        fe.extraction('tfidf')
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
        pred = prediction("SGD_en",
                          'TfidfVectorizer_en', dataset, columna_tweets)
    elif idioma == "es":
        # Inicializando clase prediction
        pred = prediction("LogisticRegression_es",
                          'CountVectorizer_es', dataset, columna_tweets)
    else:
        print("Idioma no reconocido. Terminano.")
        return
    # Iniciando Contador de tiempo
    t0 = time()
    # Ejecutando la predicción
    pred.predecir()
    # Imprimir el tiempo de ejecución
    print("TIEMPO PREDICCIÓN: ", round(time() - t0, 3), "s")


def wordcloud(nombre_wordcloud, color_fondo, idioma):
    print("=== WORDCLOUD INICIADO ===")
    # Definir ruta actual
    ruta_actual = PurePath(Path.cwd()) / 'frontend' / 'preprocesamiento'
    archivo = ruta_actual / 'TestData' / 'Output' / 'prediccion.csv'
    # Leer Predicción
    print("Lectura de Datasets")
    pred_df = pd.read_csv(archivo, encoding='ISO-8859-1')
    print(f"Cantidad Tweets Total: {pred_df.shape[0]}")
    # Leer Extracción Lematizada
    archivo = ruta_actual / 'TestData' / 'Output' / 'prediccion_wordcloud.csv'
    pred_wordcloud_df = pd.read_csv(archivo, encoding='ISO-8859-1')
    # Crearle la columna "sentimiento" al CSV de Extracción
    pred_wordcloud_df["sentiment"] = pred_df["Sentiment"]
    # Filtrar tweets por sentimiento
    pred_pos = pred_wordcloud_df[pred_df['Sentiment'] == 'positivo']
    pred_neg = pred_wordcloud_df[pred_df['Sentiment'] == 'negativo']
    pred_neu = pred_wordcloud_df[pred_df['Sentiment'] == 'neutral']
    print(f"Cantidad Tweets Positivos: {pred_pos.shape[0]}")
    print(f"Cantidad Tweets Negativos: {pred_neg.shape[0]}")
    print(f"Cantidad Tweets Neutros: {pred_neu.shape[0]}")

    # Mascara
    carpeta = Path(ruta_actual / 'DB' / 'img')
    cloud_mask = np.array(Image.open(carpeta / "cloud.png"))
    comment_mask = np.array(Image.open(carpeta / "comment.png"))
    upvote_mask = np.array(Image.open(carpeta / "upvote.png"))
    downvote_mask = np.array(Image.open(carpeta / "downvote.png"))

    # Creando WordClouds

    def crearWordCloud(dataframe, sentimiento, mask, idioma):
        # Unificar todos los textos de todas las columnas del dataframe en uno
        text = dataframe.data_lemmatized.values
        # Creando el WordCloud General
        print("Creando el WordCloud ", sentimiento)
        if idioma == 'es':
            stop = stopwords.words("spanish")
            stop_set = set(stop)
            stop_set.discard('no')
            wordcloud = WordCloud(
                width=1024, height=720, background_color=color_fondo, collocations=False, mask=mask, stopwords=stop_set).generate(str(text))
        elif idioma == 'en':
            wordcloud = WordCloud(
                width=1024, height=720, background_color=color_fondo, collocations=False, mask=mask, stopwords=STOPWORDS).generate(str(text))
        else:
            print("Idioma no reconocido: " + idioma + ". Terminando")
            return
        print("Guardando WordCloud: wordcloud_" + nombre_wordcloud + ".png")
        # Creando carpeta de WordCloud especifico
        # carpeta = Path(ruta_actual / 'TestData' / 'Output' /
        #                'WordCloud' / nombre_wordcloud)
        # if not carpeta.exists():
        #     carpeta.mkdir(exist_ok=True)
        #     print("Directorio: ", carpeta,  " creado")
        # else:
        #     print("Directorio:  ", carpeta,  " ya existe")
        ruta_img = PurePath(Path.cwd()) / 'img'
        archivo = Path(ruta_img / (
            "wordcloud_" + sentimiento + ".png"))
        wordcloud.to_file(archivo)

    crearWordCloud(pred_wordcloud_df, "general", cloud_mask, idioma)
    crearWordCloud(pred_pos, "positivo", upvote_mask, idioma)
    crearWordCloud(pred_neg, "negativo", downvote_mask, idioma)
    crearWordCloud(pred_neu, "neutral", comment_mask, idioma)
