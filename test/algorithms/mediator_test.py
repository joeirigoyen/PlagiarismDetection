from pathlib import Path
from unittest import TestCase

from src.entities.algorithms.main.cosine_algorithm import CosineAlgorithm
from src.entities.algorithms import ModelMediator, BaseModel
from src.util.config import ConfigManager


class TestModelMediator(TestCase):
    class TestModel(BaseModel):
        def __init__(self):
            super().__init__()
            self.mediator = None

        def compare_text(self, f_file_path: str | Path, s_file_path: str | Path) -> tuple[float, str]:
            return 0.0, s_file_path

        def compare_texts(self, f_dir: str | Path, s_file_path: str | Path) -> list[tuple[float, str]]:
            return [(0.0, s_file_path)]

    def setup(self, config_mgr: ConfigManager = None, json_path: str | Path = None) -> None:
        self.config = config_mgr if config_mgr else ConfigManager(json_path)
        self.mediator = ModelMediator(config_mgr=self.config)

    def test_add_child(self):
        self.setup()
        self.mediator.add_child(CosineAlgorithm())
        self.assertEqual(1, self.mediator.total_models)
        self.assertTrue(self.mediator.has_model_of_type(CosineAlgorithm))

    def test_add_children(self):
        self.setup()
        model_1, model_2 = CosineAlgorithm(), self.TestModel()
        self.mediator.add_children((model_1, model_2))
        self.assertEqual(2, self.mediator.total_models)
        self.assertTrue(self.mediator.has_model_of_type(CosineAlgorithm))
        self.assertTrue(self.mediator.has_model_of_type(self.TestModel))

    def test_compare_single(self):
        self.config = ConfigManager(Path("../resources/testConfig/test_config.json"))
        self.setup(self.config)
        self.mediator.add_child(self.TestModel())
        result = self.mediator.compare_single(self.config.get("ORIGINAL_FILES"), self.config.get("RESOURCES") / "file.txt")
        self.assertEqual(0.0, result[0])
        self.assertEqual(str(self.config.get("ORIGINAL_FILES")), result[1])
