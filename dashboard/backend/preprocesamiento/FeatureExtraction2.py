from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
import pandas as pd
import numpy as np

class FeatureExtraction2:
    def __init__(self, dataset,columna_tweets, columna_sentimiento):

        # Leer Dataset
        pd.set_option('display.max_colwidth', -1)
        tweets = pd.read_csv(dataset)
        y = tweets[columna_sentimiento]
        
        # Conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            tweets[columna_tweets], y, test_size=0.33, random_state=53)

        # Feature Extraction
        X_features_train, X_features_test, vectorizer = self.bagOfWords(X_train,X_test)

        # Upsamping SMOTE
        X_resampled, y_resampled = self.overSamplingSMOTE(X_features_train, y_train, vectorizer)

        # Modeling
        clf = self.MultiNaiveBayes(X_resampled, X_features_test, y_resampled, y_test)

    def bagOfWords(self,X_train, X_test):
        # Inicializar al objeto CountVectorizer: count_vectorizer
        count_vectorizer = CountVectorizer(stop_words='english')
        # Conjunto de Entrenamiento
        count_train = count_vectorizer.fit_transform(X_train.values.astype('U'))
        # Conjunto de pruebas
        count_test = count_vectorizer.transform(X_test.values.astype('U'))
        #print(count_vectorizer.get_feature_names()[:30])
        count_df = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())
        print(count_df.head())
        return count_train, count_test, count_vectorizer
        
    def TfidfVectorizer(self, X_train, X_test):
        # Inicializar al objeto TfidfVectorizer: tfidf_vectorizer
        tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)

        # Transformar los datos de entrenamiento: tfidf_train
        tfidf_train = tfidf_vectorizer.fit_transform(X_train.values.astype('U'))

        # Transformar los datos de prueba: tfidf_test
        tfidf_test = tfidf_vectorizer.transform(X_test.values.astype('U'))

        # Imprimir las primeros 5 características
        tfidf_df = pd.DataFrame(
            tfidf_train.A, columns=tfidf_vectorizer.get_feature_names())
        print(tfidf_df.head())
        return tfidf_train, tfidf_test, tfidf_vectorizer
    
    def MultiNaiveBayes(self, X_train, X_test, y_train, y_test):
        # Instanciar modelo MultinomialNB
        nb_classifier = MultinomialNB()
        # Entrenar el modelo
        nb_classifier.fit(X_train, y_train)
        # Predecir con el modelo
        pred = nb_classifier.predict(X_test)
        # Evaluar el modelo
        score = classification_report(y_test, pred)
        print(score)
        print(confusion_matrix(y_test, pred))
        return nb_classifier

    def overSamplingSMOTE(self, X_train, y_train, vectorizer):
        # Define the resampling method
        method = SMOTE(kind='regular')
        # Convertir X_train (Spacy Matrix a DataFrame)
        X_df = pd.DataFrame(
            X_train.A, columns=vectorizer.get_feature_names())
        # Create the resampled feature set
        X_resampled, y_resampled = method.fit_sample(X_df.to_numpy(), y_train.to_numpy())
        print(pd.value_counts(pd.Series(y_resampled)))
        return X_resampled, y_resampled


FeatureExtraction2("data_lemmatized.csv", 'data_lemmatized', "sentiment")
