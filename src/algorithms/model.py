from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self):
        self.__mediator = None

    @property
    def mediator(self):
        return self.__mediator
    
    @mediator.setter
    def mediator(self, mediator):
        self.__mediator = mediator

    @abstractmethod
    def compare_text(self, f_file_path: str, s_file_path: str) -> tuple[float, str]:
        ...
    
    @abstractmethod
    def compare_texts(self, f_dir: str, s_file_path: str) -> list[tuple[float, str]]:
        ...


class BaseMediator(ABC):
    @abstractmethod
    def add_child(self, model: BaseModel) -> None:
        ...
    
    @abstractmethod
    def add_children(self, models: tuple[BaseModel]) -> None:
        ...


class ModelMediator(BaseMediator):
    def __init__(self, *args: BaseModel):
        self.ai_models = []
        self.add_children(args)

    def add_child(self, model: BaseModel) -> None:
        model.mediator = self
    
    def add_children(self, models: tuple[BaseModel]) -> None:
        for m in models:
            self.add_child(m)


# Example
""" model_a = BaseModel()
model_b = BaseModel()
mediator = ModelMediator([model_a, model_b]) """
