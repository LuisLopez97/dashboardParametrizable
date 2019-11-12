import AnalisisSentimientos as sentimiento

# sentimiento.instalarLibrarias()
sentimiento.entrenar("Tweets_pg_prepared.csv", "text", "airline_sentiment")
# sentimiento.predecir("test.csv", "SentimentText")