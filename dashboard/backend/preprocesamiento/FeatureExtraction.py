from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from LongFunctionProgress import provide_progress_bar
from LongFunctionProgress import progress_wrapped
from imblearn.under_sampling import NearMiss
from imblearn.over_sampling import SMOTE
from pathlib import Path, PurePath
from tqdm import tqdm
from time import time
import pandas as pd
import numpy as np
import os
import pickle


class FeatureExtraction:
    def __init__(self, dataset,columna_tweets, columna_sentimiento, idioma):
        self.dataset = dataset
        self.columna_tweets = columna_tweets
        self.columna_sentimiento = columna_sentimiento
        self.idioma = idioma
        self.ruta_actual = PurePath(Path.cwd())

    def extraction(self, extractor):
        print("=== FEATURE EXTRACTION INICIADO ===")
        # Cargando rutas y lectura dataset

        # Dividir conjuntos (Entrenamiento y pruebas)
        if self.idioma == "es":
            X_train, y_train = self.path('DB', self.dataset)
            X_test, y_test = self.path('DB', 'tweets_es_development.csv')
        else:
            x, y = self.path('DB', self.dataset)
            X_train, X_test, y_train, y_test = self.split(x, y)

        # Feature Extraction
        if extractor == 'bagofwords':
            print("Feature Extraction: Bag of Words...")
            X_features_train, X_features_test, vectorizer = self.bagOfWords(
                X_train, X_test)
        elif extractor == 'tfidf':
            X_features_train, X_features_test, vectorizer = self.TfidfVectorizer(
                X_train, X_test)
        else:
            print('Extractor no seleccionado. Terminando')
            return

        # Upsamping SMOTE
        print("Upsamping SMOTE...")
        X_resampled_path = Path(self.ruta_actual / ("DB/Resampling_SMOTE/X_resampled_" + extractor))
        y_resampled_path = Path(self.ruta_actual / ("DB/Resampling_SMOTE/y_resampled_" + extractor))
        if(X_resampled_path.exists() and y_resampled_path.exists()):
            X_resampled = self.loadPickle("DB/Resampling_SMOTE/X_resampled_" + extractor)
            y_resampled = self.loadPickle("DB/Resampling_SMOTE/y_resampled_" + extractor)
        else:
            X_resampled, y_resampled = self.overSamplingSMOTE(
                X_features_train, y_train, vectorizer, extractor)
        print("=== FEATURE EXTRACTION TERMINADO ===")

        # Modeling
        print("=== MODELADO INICIADO ===")
        print("Modelado: MultinomialNB...")
        NB_clf = self.MultiNaiveBayes(X_resampled, X_features_test, y_resampled, y_test)

        print("Modelado: LogisticRegression...")
        LR_clf = self.LogisticRegression(X_resampled, X_features_test, y_resampled, y_test)

        # print("Modelado: SVM...")
        # SVM_clf = self.SVM(X_resampled, X_features_test, y_resampled, y_test)

        print("Modelado: Random Forest...")
        RF_clf = self.RandomForest(X_resampled, X_features_test, y_resampled, y_test)

        print("Modelado: Stochastic Gradient Boost...")
        SGD_clf = self.SGD(X_resampled, X_features_test, y_resampled, y_test)

        print("=== MODELADO TERMINADO ===")
        self.crearPickle(NB_clf, 'Classifiers/MultinomialNB')
        self.crearPickle(LR_clf, 'Classifiers/LogisticRegression')
        # self.crearPickle(SVM_clf, 'Classifiers/SVM')
        self.crearPickle(RF_clf, 'Classifiers/RandomForest')
        self.crearPickle(SGD_clf, 'Classifiers/SGD')


    def bagOfWords(self,X_train, X_test):
        # Inicializar al objeto CountVectorizer: count_vectorizer
        count_vectorizer = CountVectorizer()
        # Conjunto de Entrenamiento
        count_train = count_vectorizer.fit_transform(X_train.values.astype('U'))
        # Conjunto de pruebas
        count_test = count_vectorizer.transform(X_test.values.astype('U'))
        #print(count_vectorizer.get_feature_names()[:30])
        count_df = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())
        print(count_df.head())

        # Guardando como pickle
        self.crearPickle(count_vectorizer, 'Vectorizers/CountVectorizer')
        return count_train, count_test, count_vectorizer

    def TfidfVectorizer(self, X_train, X_test):
        # Inicializar al objeto TfidfVectorizer: tfidf_vectorizer
        tfidf_vectorizer = TfidfVectorizer()

        # Transformar los datos de entrenamiento: tfidf_train
        tfidf_train = tfidf_vectorizer.fit_transform(X_train.values.astype('U'))

        # Transformar los datos de prueba: tfidf_test
        tfidf_test = tfidf_vectorizer.transform(X_test.values.astype('U'))

        # Imprimir las primeros 5 características
        tfidf_df = pd.DataFrame(
            tfidf_train.A, columns=tfidf_vectorizer.get_feature_names())
        print(tfidf_df.head())

        # Guardando como pickle
        self.crearPickle(tfidf_vectorizer, 'Vectorizers/TfidfVectorizer')
        return tfidf_train, tfidf_test, tfidf_vectorizer

    @progress_wrapped(estimated_time=100)
    def overSamplingSMOTE(self, X_train, y_train, vectorizer, extractor):
        # Define the resampling method
        method = SMOTE(kind='regular')
        # Convertir X_train (Spacy Matrix a DataFrame)
        X_df = pd.DataFrame(
            X_train.A, columns=vectorizer.get_feature_names())
        # Create the resampled feature set
        X_resampled, y_resampled = method.fit_sample(X_df.to_numpy(), y_train.to_numpy())
        print(pd.value_counts(pd.Series(y_resampled)))
        # Guardar en Pickles
        self.crearPickle(X_resampled, "DB/Resampling_SMOTE/X_resampled_" + extractor)
        self.crearPickle(y_resampled, "DB/Resampling_SMOTE/y_resampled_" + extractor)
        return X_resampled, y_resampled

    def MultiNaiveBayes(self, X_train, X_test, y_train, y_test):
        # Instanciar modelo MultinomialNB
        nb_classifier = MultinomialNB()
        # Medicion del tiempo de entrenamiento
        t0 = time()
        # Entrenar el modelo
        nb_classifier.fit(X_train, y_train)
        # Impresion del tiempo de entrenamiento
        print("training time", round(time() - t0, 3), "s")
        # Predecir con el modelo
        pred = nb_classifier.predict(X_test)
        # Evaluar el modelo
        score = classification_report(y_test, pred)
        print(score)
        print(confusion_matrix(y_test, pred))
        return nb_classifier

    def LogisticRegression(self, X_train, X_test, y_train, y_test):
        # Instanciar modelo LogisticRegression
        lr_classifier = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
        # Medicion del tiempo de entrenamiento
        t0 = time()
        # Entrenar el modelo
        lr_classifier.fit(X_train, y_train)
        # Impresion del tiempo de entrenamiento
        print("training time", round(time() - t0, 3), "s")
        # Predecir con el modelo
        pred = lr_classifier.predict(X_test)
        # Evaluar el modelo
        score = classification_report(y_test, pred)
        print(score)
        print(confusion_matrix(y_test, pred))
        return lr_classifier

    def SVM(self, X_train, X_test, y_train, y_test):
        # Instanciar modelo SVC
        svm_classifier = SVC(kernel='linear')
        # Medicion del tiempo de entrenamiento
        t0 = time()
        # Entrenar el modelo
        svm_classifier.fit(X_train, y_train)
        # Impresion del tiempo de entrenamiento
        print("training time", round(time() - t0, 3), "s")
        # Predecir con el modelo
        pred = svm_classifier.predict(X_test)
        # Evaluar el modelo
        score = classification_report(y_test, pred)
        print(score)
        print(confusion_matrix(y_test, pred))
        return svm_classifier

    def SGD(self, X_train, X_test, y_train, y_test):
        # Instanciar modelo SGD
        sgd_classifier = SGDClassifier(max_iter=1000, tol=1e-3)
        # Medicion del tiempo de entrenamiento
        t0 = time()
        # Entrenar el modelo
        sgd_classifier.fit(X_train, y_train)
        # Impresion del tiempo de entrenamiento
        print("training time", round(time() - t0, 3), "s")
        # Predecir con el modelo
        pred = sgd_classifier.predict(X_test)
        # Evaluar el modelo
        score = classification_report(y_test, pred)
        print(score)
        print(confusion_matrix(y_test, pred))
        return sgd_classifier

    def RandomForest(self, X_train, X_test, y_train, y_test):
        # Instanciar modelo RandomForest
        rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0)
        # Medicion del tiempo de entrenamiento
        t0 = time()
        # Entrenar el modelo
        rf_classifier.fit(X_train, y_train)
        # Impresion del tiempo de entrenamiento
        print("training time", round(time() - t0, 3), "s")
        # Predecir con el modelo
        pred = rf_classifier.predict(X_test)
        # Evaluar el modelo
        score = classification_report(y_test, pred)
        print(score)
        print(confusion_matrix(y_test, pred))
        return rf_classifier


    def path(self, carpeta, dataset):
        # Direccion Pickle Clasificador
        _archivo = self.ruta_actual / carpeta / dataset
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

    def crearPickle(self, obj , archivo):
        # Guardando como pickle
        print(f"Pickle: {archivo}...")
        # Direccion Pickle Clasificador
        _archivo = self.ruta_actual / archivo
        with open(_archivo, 'wb') as pickleFile:
            pickle.dump(obj, pickleFile)
        print(f"Pickle: {archivo} guardado con éxito!")

    def loadPickle(self, archivo_pickle):
        _archivo = self.ruta_actual / archivo_pickle
        print(f"Abriendo Pickle {archivo_pickle}...")
        with open(_archivo, 'rb') as infile:
            obj = pickle.load(infile)
        print(f"Pickle {archivo_pickle} abierto con exito")
        return obj

# FeatureExtraction2("data_lemmatized.csv", 'data_lemmatized', "sentiment")
