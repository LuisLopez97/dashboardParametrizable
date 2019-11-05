from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
from longFunctionProgress import provide_progress_bar
from longFunctionProgress import progress_wrapped
from tqdm import tqdm
import pandas as pd
import numpy as np
import os
import pickle


class FeatureExtraction:
    def __init__(self, dataset,columna_tweets, columna_sentimiento):
        self.dataset = dataset
        self.columna_tweets = columna_tweets
        self.columna_sentimiento = columna_sentimiento

    def extraction(self):
        print("=== FEATURE EXTRACTION INICIADO ===")
        # Cargando rutas y lectura dataset
        x, y = self.path('DB')

        # Dividir conjuntos (Entrenamiento y pruebas)
        X_train, X_test, y_train, y_test = self.split(x, y)

        # Feature Extraction
        print("Feature Extraction: Bag of Words...")
        X_features_train, X_features_test, vectorizer = self.bagOfWords(
            X_train, X_test)

        # Upsamping SMOTE
        print("Upsamping SMOTE...")
        X_resampled, y_resampled = self.overSamplingSMOTE(
            X_features_train, y_train, vectorizer)

        # Modeling
        print("Modelado: MultinomialNB...")
        clf = self.MultiNaiveBayes(X_resampled, X_features_test, y_resampled,
                                   y_test)

        # Guardando como pickle
        print(f"Guardando pickle: clf...")
        # Training Set
        cur_path = os.path.dirname(__file__)
        _archivo = os.path.join(cur_path, 'Classifiers', "MultinomialNB")
        with open(_archivo, 'wb') as pickleFile:
            pickle.dump(clf, pickleFile)
        print(f"¡Pickle guardado con éxito!")
        print("=== FEATURE EXTRACTION TERMINADO ===")

    def path(self, carpeta):
        # Cargando rutas
        cur_path = os.path.dirname(__file__)
        _archivo = os.path.join(cur_path, carpeta, self.dataset)
        # Leer Dataset
        print("Leyendo Dataset...")
        pd.set_option('display.max_colwidth', -1)
        tweets = pd.read_csv(_archivo)
        x = tweets[self.columna_tweets]
        y = tweets[self.columna_sentimiento]
        return x, y

    def split(self, x, y):
        # Conjunto de entrenamiento y prueba
        print("Creando conjunto de entrenamiento y prueba...")
        X_train, X_test, y_train, y_test = train_test_split(
            x, y, test_size=0.33, random_state=53)
        return X_train, X_test, y_train, y_test


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

        # Guardando como pickle
        print(f"Guardando pickle: vectorizer...")
        # Training Set
        cur_path = os.path.dirname(__file__)
        _archivo = os.path.join(cur_path, 'Vectorizers', "CountVectorizer")
        with open(_archivo, 'wb') as pickleFile:
            pickle.dump(count_vectorizer, pickleFile)
        print(f"¡Pickle guardado con éxito!")

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

    @progress_wrapped(estimated_time=100)
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


# FeatureExtraction2("data_lemmatized.csv", 'data_lemmatized', "sentiment")
