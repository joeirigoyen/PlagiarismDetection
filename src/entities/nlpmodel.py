from pathlib import Path

from src.entities.model import Model
from src.entities.textdata import TextData, TextDataDirectory

class NLPModel(Model):
    def __init__(self, data: TextData | TextDataDirectory, source_dir: Path):
        super().__init__("nlp", data)
        self.source_dir = source_dir

    def tokenize_text(self, text: TextData) -> list[str]:
        """
        Tokenize the text.
        """
        return text.tokenize()

    def check(self, params: dict, source_dir: Path) -> None:
        # Perform preprocessing on suspicious text
        self.preprocess(params.get("preprocess"))
        # Perform preprocessing on source texts
        source_texts = TextDataDirectory(source_dir)
        source_texts.preprocess(params.get("preprocess"))
        # Calculate distance between suspicious text and source texts


