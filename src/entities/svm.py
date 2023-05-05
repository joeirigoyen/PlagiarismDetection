from os import path
from pathlib import Path
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from src.entities.textdata import TextDataDirectory, TextData
import pandas as pd
import nltk
import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans


class SVMModel:
    def __init__(self, text_data: TextData) -> None:
        self.text_data = text_data.data

    def get_vectors(self, params: dict) -> CountVectorizer | TfidfVectorizer:
        max_grams = params.get("ngrams", 8)
        vec_type = params.get("vectorizer", "count")
        match vec_type:
            case "count": return CountVectorizer(analyzer='word', ngram_range=(1, max_grams), stop_words='english', max_df=0.2, min_df=5, max_features=60)
            case "tfidf": return TfidfVectorizer(analyzer='word', ngram_range=(1, max_grams), stop_words='english', max_df=0.2, min_df=5, max_features=60)
            case _: return CountVectorizer(analyzer='word', ngram_range=(1, max_grams), stop_words='english', max_df=0.2, min_df=5, max_features=60)


    def vectorize(self, data: list, params: dict) -> list:
        vectorizer = self.get_vectors(params)
        vectors = vectorizer.fit_transform(data)
        return vectors


    def predict(self, params: dict, train: bool = False) -> None:
        model_name = params.get("model", "svm")
        
        nltk.download('stopwords', quiet=True)

        original_path =  Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / "original"
        original = TextDataDirectory(original_path)

        suspicious_path = Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / "suspicious"
        suspicious = TextDataDirectory(suspicious_path)

        df = pd.DataFrame(columns=['document', 'label'])
        datas = original.data + suspicious.data
        labels = [0 for _ in range(len(original.data))] + [1 for _ in range(len(suspicious.data))]
        texts = [text.data for text in datas]
        df['document'] = texts
        df['label'] = labels

        if not train:
            texts.append(self.text_data)
        
        vectors = self.vectorize(texts, params)
        test_vector = None
        if not train:
            texts.pop()
            num_rows, _ = vectors.shape
            test_vector = vectors[num_rows-1, :]
            vectors = vectors[:num_rows-1, :]

        X_train, X_test, y_train, y_test = train_test_split(vectors, df['label'], test_size=0.2,random_state=42)
        
        scaler = StandardScaler(with_mean=False)
        if model_name == "naive_bayes":
            X_train = scaler.fit_transform(X_train).toarray()
            X_test = scaler.transform(X_test).toarray()
            if not train:
                test_vector = scaler.transform(test_vector).toarray()
        else:
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            if not train:
                test_vector = scaler.transform(test_vector)

        if train:
            match model_name:
                case "linear_svc": model = svm.LinearSVC()
                case "naive_bayes": model = GaussianNB()
                case "random_forest": model = RandomForestClassifier(max_depth=20, random_state=42, n_estimators=200, n_jobs=-1)
                case "kmeans": model = KMeans(n_clusters=2, random_state=42, n_init="auto")
                case _: model = svm.LinearSVC()

            model.fit(X_train, y_train)

            joblib.dump(model, Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / f"{model_name}.pkl")
        
            y_pred = model.predict(X_test)

            print("Accuracy:",f'{metrics.accuracy_score(y_test, y_pred) * 100:.2f}%')

            print("Precision:", f'{metrics.precision_score(y_test, y_pred, average="weighted"):.2f}')

            print("Recall:",f'{metrics.recall_score(y_test, y_pred, average="weighted"):.2f}')

            print('Confusion matrix:',metrics.confusion_matrix(y_test, y_pred))

        else:
            model_name = params.get("model", "linear_svc")
            model = joblib.load(Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("resources") / f"{model_name}.pkl")

            y_pred = model.predict(test_vector)
            if hasattr(model, "decision_function"):
                confidence = model.decision_function(test_vector)
            elif hasattr(model, "predict_proba"):
                confidence = model.predict_proba(test_vector)[:, 1]
            else:
                confidence = None

            print("Predicted label:", "File is not plagiarized" if y_pred == 0 else "File is plagiarized")
            if confidence is not None:
                print("Confidence:", confidence)