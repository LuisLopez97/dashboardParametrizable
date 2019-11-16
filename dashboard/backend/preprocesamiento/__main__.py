import AnalisisSentimientos as sentimiento

# sentimiento.instalarLibrarias()
""" extraccion(idioma, palabra, tiempo_segundos) """
sentimiento.extraccion("en", "fortnite", 180)

"""entrenar(dataset, columna_tweets, columna_sentimiento, idioma)"""
# sentimiento.entrenar("tweets_en.csv", "text", "airline_sentiment", "en")
# sentimiento.entrenar("tweets_es.csv", "content", "sentiment", "es")
"""predecir(dataset, columna_tweets)"""
sentimiento.predecir("extraccion_tweets.csv", "Text", "en")
# sentimiento.predecir("extraccion_tweets.csv", "Text", "es")
