from src.entities.model import Model
from src.entities.textdata import TextData, TextDataDirectory

class NLPModel(Model):
    def __init__(self, data: TextData | TextDataDirectory):
        super().__init__("nlp", data)
