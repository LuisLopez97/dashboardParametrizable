import AnalisisSentimientos as sentimiento

sentimiento.entrenar("Tweets_pg_prepared.csv", "text", "airline_sentiment")
sentimiento.predecir("test.csv", "SentimentText")