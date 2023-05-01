import json

from src.entities.algorithms.main.cosine_algorithm import CosineAlgorithm
from src.entities.algorithms import ModelMediator
from src.util.config import ConfigManager


if __name__ == '__main__':
    # Get global variables
    cm = ConfigManager()
    ground_truth = json.load(open(cm.get("GROUND_TRUTH"), "r"))
    # Create mediator
    mediator = ModelMediator()
    # mediator.add_child(CosineAlgorithm())
    mediator.add_child(CosineAlgorithm(vec_type="tfidf"))
    # Compare files
    mediator.run_comparison(show_ground_truth=True)
