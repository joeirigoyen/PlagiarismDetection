from nltk.metrics.distance import jaccard_distance
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from src.entities.model import Model
from src.entities.textdata import TextData, TextDataDirectory


class NLPModel(Model):
    def __init__(self, data: TextData | TextDataDirectory, candidates: list[tuple]):
        super().__init__("nlp", data)
        self.candidates = candidates
        self.source_dir = self.get_text_data_dir(candidates)

    @staticmethod
    def get_text_data_dir(candidates: list[tuple]) -> TextDataDirectory:
        """
        Get the directory of the source texts.
        """
        candidate_list = []
        for candidate in candidates:
            content = Path(candidate[0]).read_text(encoding="utf-8")
            candidate_list.append(TextData(content))
        return TextDataDirectory(candidate_list)

    @staticmethod
    def get_vectors_distance(vec_1: list, vec_2: list, method: str) -> float:
        """
        Get the distance between two vectors.
        """
        match method:
            case "cosine":
                return cosine_similarity(vec_1, vec_2)[0][0]
            case "euclidean":
                return euclidean_distances(vec_1, vec_2)[0][0]
            case _:
                return cosine_similarity(vec_1, vec_2)[0][0]

    def get_ngrams_distance(self, params: dict) -> list:
        """
        Calculates the distance between two texts using ngrams.
        :param params: The parameters for the calculation given by the user.
        :return: The result of the calculation for each source file.
        """
        result = []
        ngrams = params.get("ngrams") or 8
        tokenized_sus = self.data.get_ngrams(ngrams)
        for index, source in enumerate(self.source_dir.data):
            tokenized_src = source.get_ngrams(ngrams)
            filename = self.candidates[index][0]
            score = float((100 * (1 - jaccard_distance(tokenized_sus, tokenized_src))))
            result.append((filename, score))
        return result

    def get_tokens_distance(self, params: dict) -> list:
        """
        Calculates the distance between two texts using vectorization tokens.
        :return: The result of the calculation for each source file.
        """
        result = []
        for index, source in enumerate(self.source_dir.data):
            corpus = [self.data.data, source.data]
            match params.get("vectorizer"):
                case "count":
                    vectorizer = CountVectorizer(analyzer="word", ngram_range=(2, 8))
                case "tfidf":
                    vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(2, 8))
                case _:
                    vectorizer = CountVectorizer(analyzer="word", ngram_range=(2, 8))
            transform = vectorizer.fit_transform(corpus)
            vector_1 = transform.toarray()[0].reshape(1, -1)
            vector_2 = transform.toarray()[1].reshape(1, -1)
            score = self.get_vectors_distance(vector_1, vector_2, params.get("distance"))
            filename = self.candidates[index][0]
            result.append((filename, score))
        return result

    @staticmethod
    def analyze(params: dict, result: list) -> None:
        """
        Print a report of the result.
        :param params: The parameters for the calculation given by the user.
        :param result: The result of the calculation for each source file.
        """
        max_result = max(result, key=lambda x: x[1])
        print(f"Most similar file: {max_result[0]}")
        match params.get("preprocess"):
            case "stem" | "lemmatize":
                threshold = params.get("threshold") or 10.0
                print(f"Similarity score: {max_result[1]} (using {params.get('distance') or 'cosine'} distance)")
                print(f"File is {'not ' if max_result[1] < threshold else ''}potentially plagiarized")
            case "stopwords" | "unpunctuate" | _:
                threshold = params.get("threshold") or 0.6
                print(f"Similarity score: {max_result[1]} (using {params.get('distance') or 'cosine'} distance)")
                print(f"File is {'not ' if max_result[1] < threshold else ''}potentially plagiarized")

    def check(self, params: dict) -> None:
        # Perform preprocessing on suspicious text
        self.preprocess(params.get("preprocess"))
        # Perform preprocessing on source texts
        preprocessing_method = params.get("preprocess")
        self.source_dir.preprocess(preprocessing_method)
        # Tokenize suspicious text
        match preprocessing_method:
            case "stem" | "lemmatize":
                result = self.get_ngrams_distance(params)
            case "stopwords" | "unpunctuate":
                result = self.get_tokens_distance(params)
            case _:
                result = self.get_ngrams_distance(params)
        # Sort the result
        self.analyze(params, result)
