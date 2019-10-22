# Importacion de librerias
import numpy as np
import pandas as pd
import nltk
import csv
from sklearn.utils import resample
import ast
import json

class FeatureExtraction:
    word_features = []
    train_set_upsampled = []
    test_set = []
    archivo = ""
    columna_texto = ""
    columna_sentimiento = ""

    def __init__(self, archivo, columna_texto, columna_sentimiento):
        self.archivo = archivo
        self.columna_texto = columna_texto
        self.columna_sentimiento = columna_sentimiento
        self.crearConjuntos()

    def crearConjuntos(self):
        # Permite desplegar el texto completo en Jupyter y en Terminal
        pd.set_option('display.max_colwidth', -1)

        # Lectura de CSV
        data = pd.read_csv(self.archivo)
        data_lemmatized = data[self.columna_texto]
        self.word_features = self.bagOfWords(data_lemmatized)
        
        # Conjunto de Entrenamiento y Pruebas
        porcentaje = int(len(data_lemmatized) * .20)
        train_set, self.test_set = data[porcentaje:], data[:porcentaje]
        self.train_set_upsampled = self.resampling(train_set, self.columna_sentimiento)

        # Guardar conjunto de entrenamiento y pruebas en CSV
        train_csv = pd.DataFrame(self.train_set_upsampled).to_csv (r'train_set_upsampled.csv', index = None, header=True)
        test_csv = pd.DataFrame(self.test_set).to_csv (r'test_set.csv', index = None, header=True)

    # Crear un Bag of Words
    def bagOfWords(self, tweets_lematizados):
        l = tweets_lematizados.tolist()        # Convertir Series a Lista
        all_words = []
        for linea in l:                     # Extraer todas las palabras
            lista = str(linea).split()
            all_words += lista
            
        # Utilizar FreqDist para encontrar las palabras más utilizadas en todos los documentos
        all_words_freq = nltk.FreqDist(all_words)

        # Y tomar los primeros 2000 más frecuentes
        return list(all_words_freq)[:2000]



    # Definir el feature extractor
    def document_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features['contains({})'.format(word)] = (word in document_words)
        return features



    # Resampling
    def resampling(self, train_set, columna_sentimiento):
        # Obtener los sentimientos en el dataframe y la cantidad que existen
        contador_sentimientos = train_set[columna_sentimiento].value_counts()

        # Obtener la cantidad más grande
        mayor = contador_sentimientos.max()

        # Obtener el sentimiento con dicha cantidad grande
        for items in contador_sentimientos.iteritems():
            if items[1] == mayor:
                sentimiento_mayor = items[0]
                
        # Borrar el sentimiento más grande de la lista
        del(contador_sentimientos[sentimiento_mayor])

        # Obtener los otros dos sentimientos que son menores
        lista_contador_sentimientos = contador_sentimientos.keys()

        # Separate majority and minority classes
        df_majority = train_set[train_set.sentiment == sentimiento_mayor]
        df_minority_1 = train_set[train_set.sentiment == lista_contador_sentimientos[0]]
        df_minority_2 = train_set[train_set.sentiment == lista_contador_sentimientos[1]]
        
        # Upsample minority class
        df_upsampled_1 = resample(df_minority_1, 
                                        replace=True,     # sample with replacement
                                        n_samples=mayor,    # to match majority class
                                        random_state=123) # reproducible results

        df_upsampled_2 = resample(df_minority_2, 
                                        replace=True,     # sample with replacement
                                        n_samples=mayor,    # to match majority class
                                        random_state=123) # reproducible results
        
        # Combine majority class with upsampled minority class
        train_upsampled = pd.concat([df_majority, df_upsampled_1, df_upsampled_2])
        return train_upsampled


    # Preparar los features del conjunto de entrenamiento y pruebas
    def featuresPreparation(self, train_upsampled_file, test_set_file):
        # Leer CSV con los archivos del conjunto de entrenamiento y prueba sin features
        train_set = pd.read_csv(train_upsampled_file)
        test_set = pd.read_csv(test_set_file)
        # Convertir el conjunto de entrenamiento y pruebas a una listas
        train = train_set.values.tolist()
        test = test_set.values.tolist()


        # Crear los conjuntos de entrenamiento y prueba con las carácterísticas (pivoteo de Bag of Words)
        train_feature_sets = [(self.document_features(str(d)), c) for (d,c) in train]
        test_feature_sets = [(self.document_features(str(d)), c) for (d,c) in test]
        
        # Guardar como JSON
        #with open('train_feature_column.json', 'w') as jsonFile:
        #    for lists in train_feature_sets:
        #        json.dump(lists[0] , jsonFile)

        train_sentiment_csv = pd.DataFrame(train_feature_sets).to_csv (r'train_feature_sets.csv', index = None, header=True)
        test_csv = pd.DataFrame(test_feature_sets).to_csv (r'test_feature_sets.csv', index = None, header=True)


    def modeling(self, train_csv, test_csv):
        # Read CSV with train and test features
        feature_train = pd.read_csv(train_csv)
        feature_test = pd.read_csv(test_csv)

        # convertir primera columna a diccionario
        feature_train['0'] = feature_train['0'].apply(ast.literal_eval)
        feature_test['0']  = feature_test['0'].apply(ast.literal_eval)

        feature_train_list = feature_train.values.tolist()
        feature_test_list = feature_test.values.tolist()

        print(feature_test_list[:2][:])
        # Train de model (Naive Bayes)
        classifier = nltk.NaiveBayesClassifier.train(feature_train_list)
        
        # Evaluate the training with Accuracy score
        print(nltk.classify.accuracy(classifier, feature_test_list))

        # Print 100 most significative words in analysis
        print(classifier.show_most_informative_features(100))


#fe = FeatureExtraction("data_lemmatized.csv", "data_lemmatized", "sentiment")
#fe.featuresPreparation("train_set_upsampled.csv", 'test_set.csv')
#fe.modeling("train_feature_sets.csv", "test_feature_sets.csv")