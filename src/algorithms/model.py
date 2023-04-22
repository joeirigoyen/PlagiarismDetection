from abc import ABC, abstractmethod
from pathlib import Path

from src.util.config import ConfigManager
from src.util.ioutils import get_user_input, load_from_json_file
from src.util.file_manager import FileManager as Fm


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
    def compare_text(self, f_file_path: str | Path, s_file_path: str | Path) -> tuple[float, str]:
        ...
    
    @abstractmethod
    def compare_texts(self, f_dir: str | Path, s_file_path: str | Path) -> list[tuple[float, str]]:
        ...

    @staticmethod
    def get_max_similarity(results: list[tuple[float, str]]) -> tuple[float, str]:
        """
        Returns the file with the highest similarity.
        :param results: A list of tuples containing the cosine similarity between the two documents and the original document's path.
        :return: A tuple containing the cosine similarity between the two documents and the original document's path.
        """
        return max(results, key=lambda x: x[0])


class BaseMediator(ABC):
    @abstractmethod
    def add_child(self, model: BaseModel) -> None:
        ...
    
    @abstractmethod
    def add_children(self, models: tuple[BaseModel]) -> None:
        ...


class ModelMediator(BaseMediator):
    def __init__(self, *args: BaseModel, config_mgr: ConfigManager = ConfigManager()):
        self.__models: list[BaseModel] = []
        self.__config_manager = config_mgr
        self.__ground_truth = load_from_json_file(self.__config_manager.get("GROUND_TRUTH"))
        self.__cm = ConfigManager()
        self.add_children(args)

    def add_child(self, model: BaseModel) -> None:
        model.mediator = self
        self.__models.append(model)
    
    def add_children(self, models: tuple[BaseModel]) -> None:
        for m in models:
            self.add_child(m)

    def compare_single(self, original_text: str | Path, suspicious_text: str | Path) -> tuple[float, str]:
        """
        Returns the average results of all of the child models' comparison results.
        :param original_text:
        :param suspicious_text:
        :return: A tuple containing the average results of all of the child models' comparison results and the original document's path.
        """
        model_sum = 0
        for model in self.__models:
            model_result = model.compare_text(original_text, suspicious_text)
            model_sum += model_result[0]
        return model_sum / len(self.__models), str(original_text)

    def compare_dir(self, original_dir: str | Path, suspicious_text: str | Path) -> tuple[float, str]:
        """
        Compares all the files in a directory against a single file. Returns the file with the highest similarity according to the average calculated using this class' compare_single() method.
        :param original_dir:
        :param suspicious_text:
        :return: A tuple containing the cosine similarity between the two most similar documents and the original document's path.
        """
        results = []
        for child in Path(original_dir).iterdir():
            if child.is_file():
                res = self.compare_single(child, suspicious_text)
                results.append(res)
        return BaseModel.get_max_similarity(results)

    def run_comparison(self, alternative_path: str | Path = None, show_ground_truth: bool = False) -> None:
        """
        Runs a batch comparison between all the files in a directory and a single file using the child models.
        :return:
        """
        sus_dir = self.__cm.get("SUSPICIOUS_FILES") if not alternative_path else alternative_path
        if Fm.validate_file(sus_dir):
            size, correct = 0, 0
            for f in sus_dir.iterdir():
                if f.is_file():
                    result = self.compare_dir(self.__cm.get("ORIGINAL_FILES"), f)
                    # Check results
                    file_stem = Fm.extract_file_name(f)
                    expected = self.__ground_truth[file_stem]
                    is_plag = result[0] > 60.0
                    # Show main results
                    print(f"{file_stem}".center(20, '-'))
                    print(f"Results: {is_plag} ({result[0]:2f}% similarity with {result[1]})")
                    if show_ground_truth:
                        size += 1
                        if is_plag == expected:
                            correct += 1
                        # Print results
                        if file_stem in self.__ground_truth.keys():
                            print(f"Expected result: {self.__ground_truth.get(file_stem)}")
                        else:
                            print(f"No ground truth found for file {file_stem}")
            if show_ground_truth:
                print(f"Accuracy: {correct / size * 100:2f}%")
