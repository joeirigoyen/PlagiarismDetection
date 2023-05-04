from src.entities.textdata import TextData, TextDataDirectory
from abc import ABC, abstractmethod
from src.cli.ioutils import perr

class Model(ABC):
    def __init__(self, name: str, data: TextData | TextDataDirectory) -> None:
        self.name = name
        self.data = data


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