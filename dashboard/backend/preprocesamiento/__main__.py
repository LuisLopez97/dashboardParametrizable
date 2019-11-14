import AnalisisSentimientos as sentimiento

# sentimiento.instalarLibrarias()
sentimiento.entrenar("tweets_es.csv", "content", "sentiment", "es")
# sentimiento.predecir("test.csv", "SentimentText")
