from frontend.preprocesamiento import AnalisisSentimientos as sentimiento
import datetime as dt
palabra = "Iran"
# sentimiento.instalarLibrarias("frontend/preprocesamiento/requirements.txt")

""" extraccion(idioma, palabra, tiempo_segundos) """
# sentimiento.extraccionTiempoReal( palabra, "en", 60*10 )
""" extraccionHistorico(palabra, idioma, limite_tweets, fecha_inicio, fecha_final, bins) """
sentimiento.extraccionHistorico(
palabra, limite_tweets=10000, idioma="en", fecha_inicio=dt.date(2019, 11, 15))

"""entrenar(dataset, columna_tweets, columna_sentimiento, idioma)"""
# sentimiento.entrenar("tweets_en.csv", "text", "airline_sentiment", "en")
# sentimiento.entrenar("tweets_es.csv", "content", "sentiment", "es")

"""predecir(dataset, columna_tweets)"""
sentimiento.predecir("extraccion_tweets.csv", "Text", "en")
# sentimiento.predecir("extraccion_tweets.csv", "Text", "es")

"""wordcloud(nombre_archivo, color_fondo)"""
sentimiento.wordcloud(palabra, "white", 'es')
