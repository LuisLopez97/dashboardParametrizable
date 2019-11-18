import AnalisisSentimientos as sentimiento
palabra = "fortnite"
# sentimiento.instalarLibrarias()
""" extraccion(idioma, palabra, tiempo_segundos) """
# sentimiento.extraccion("en", palabra , 60*10)

"""entrenar(dataset, columna_tweets, columna_sentimiento, idioma)"""
# sentimiento.entrenar("tweets_en.csv", "text", "airline_sentiment", "en")
# sentimiento.entrenar("tweets_es.csv", "content", "sentiment", "es")
"""predecir(dataset, columna_tweets)"""
# sentimiento.predecir("extraccion_tweets.csv", "Text", "en")
# sentimiento.predecir("extraccion_tweets.csv", "Text", "es")

"""wordcloud(nombre_archivo, color_fondo)"""
sentimiento.wordcloud(palabra, "white")
