import AnalisisSentimientos as sentimiento
from time import time 
t0 = time()
sentimiento.entrenar("Tweets_pg_prepared.csv", "text", "airline_sentiment")
print("TIEMPO COMPLETO: ", round(time() - t0, 3), "s")
# sentimiento.predecir("test.csv", "SentimentText")