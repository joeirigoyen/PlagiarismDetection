from os import path
from pathlib import Path
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from src.entities.textdata import TextDataDirectory, TextData
import pandas as pd
import nltk
import joblib
import numpy as np

class SVMModel:
    def __init__(self):
        pass

        

    def train(self) -> None:
        nltk.download('stopwords', quiet=True)

        original_path =  Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / "original"
        original = TextDataDirectory(original_path)

        suspicious_path = Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / "suspicious"
        suspicious = TextDataDirectory(suspicious_path)

        original.remove_punctuation()
        original.remove_stopwords()
        suspicious.remove_punctuation()
        suspicious.remove_stopwords()

        df = pd.DataFrame(columns=['document', 'label'])
        datas = original.data + suspicious.data
        labels = [0 for _ in range(len(original.data))] + [1 for _ in range(len(suspicious.data))]
        texts = [text.data for text in datas]
        df['document'] = texts
        df['label'] = labels

        vectorizer = CountVectorizer(analyzer='word', ngram_range=(2, 8))
        vectors = vectorizer.fit_transform(texts)

        X_train, X_test, y_train, y_test = train_test_split(vectors, df['label'], test_size=0.2,random_state=42)

        # Scale the data using StandardScaler
        scaler = StandardScaler(with_mean=False)
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)


        #Create a svm Classifier
        model = svm.LinearSVC()
        model.fit(X_train, y_train)
        joblib.dump(model, Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / "svm_model.pkl")\
        
        print(type(X_test))
        y_pred = model.predict(X_test)

        print("Accuracy:",f'{metrics.accuracy_score(y_test, y_pred) * 100:.2f}%')

        print("Precision:", f'{metrics.precision_score(y_test, y_pred):.2f}')

        print("Recall:",f'{metrics.recall_score(y_test, y_pred):.2f}')

        print('Confusion matrix:',metrics.confusion_matrix(y_test, y_pred))
    

    def predict(self, text: str) -> int:
        model = joblib.load(Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / "svm_model.pkl")
        vectorizer = CountVectorizer(analyzer='word', ngram_range=(2, 8))
        scaler = StandardScaler(with_mean=False)

        # preprocess the text
        text_processed = TextData(text)
        text_processed.remove_punctuation()
        text_processed.remove_stopwords()

        
        # fit the vectorizer on the training data and transform the test data
        original_path =  Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / "original"
        original = TextDataDirectory(original_path)
        original.remove_punctuation()
        original.remove_stopwords()


        texts_train = [text.data for text in original.data]
        vectors_train = vectorizer.fit_transform(texts_train)
        scaler.fit_transform(vectors_train)
        text_vector = vectorizer.transform([text_processed])
        text_vector = scaler.transform(text_vector)

        # predict the label using the trained model
        label = model.predict(text_vector)[0]
        return label


t = SVMModel()
t.train()
t.predict("The rise of extreme machine learning as a revolutionary learning algorithm has emphasized it in hidden solitary flow networks. Kernel-based extreme learning machine (KELM) has proven itself in several applications where the service map functions of hidden nodes are hidden from users. Conventional KELM algorithms only involve separate kernel layers, simulating shallow learning architectures for function transformations. The trend of transferring basic learning models to deep learning architectures opens up new perspectives for machine learning domains. This document tests a kernel deep learning method on traditional foundational architectures. Rising arc-cosine nuclei are better able to simulate the dominant deep-layer framework. Unlike other kernels, such as linear, polynomial, and Gaussian kernels, arc-cos kernels are inherently recursive and can express multi-layer computations in learning models. This paper examines the possibility of building a new deep kernel engine using extreme machine learning and a multi-layered arc-cos kernel. This framework outperforms traditional KELM and deep support vector machines in terms of accuracy and training time.")
