from src.entities.textdata import TextData, TextDataDirectory
from abc import ABC, abstractmethod
from src.cli.ioutils import perr

class Model(ABC):
    def __init__(self, name: str, data: TextData | TextDataDirectory) -> None:
        self.name = name
        self.data = data

    @staticmethod
    def calculate_text_distance(dist_type: str, text_1: TextData, text_2: TextData) -> float | None:
        """
        Calculates the distance between two texts.
        """
        match dist_type:
            case "cosine":
                return text_1.cosine_distance(text_2)
            case "jaccard":
                return text_1.jaccard_distance(text_2)
            case "euclidean":
                return text_1.euclidean_distance(text_2)
            case _:
                perr(f"Invalid distance type: {dist_type}")
                return None

    def preprocess(self, types: list[str]) -> None:
        for t in types:
            match t:    
                case "remove_punctuation":
                    self.data.remove_punctuation()
                case "remove_stopwords":
                    self.data.remove_stopwords()
                case "lemmatize":
                    self.data.lemmatize()
                case "stem":
                    self.data.stem()
                case _:
                    perr(f"Invalid preprocessing type: {t}")

    @abstractmethod
    def check(self) -> None:
        pass