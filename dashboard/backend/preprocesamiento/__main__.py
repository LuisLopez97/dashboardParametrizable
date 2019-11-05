from Preprocesamiento import Preprocesamiento as preprocesamiento
from FeatureExtraction2 import FeatureExtraction as feature_extraction
from Prediction import Prediction as prediction
import subprocess
import sys
import pandas as pd
import os



def importLibraries():
    subprocess.call([sys.executable, "-m", "pip", "install","-r", "requirements.txt"])

def main():
    # importLibraries()
    # prep = preprocesamiento("Tweets_pg_prepared.csv", "text", "airline_sentiment")
    # prep.preparacion()
    # fe = feature_extraction("data_lemmatized.csv", 'data_lemmatized', "sentiment")
    # fe.extraction()
    pred = prediction("MultinomialNB", 'CountVectorizer', "test.csv")
    pred.predecir()


main()