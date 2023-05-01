from src.entities.algorithms.main.cosine_algorithm import CosineAlgorithm
from src.entities.algorithms import ModelMediator
from src.util.ioutils import get_user_input


if __name__ == '__main__':
    # Create mediator
    mediator = ModelMediator()
    # mediator.add_child(CosineAlgorithm())
    mediator.add_child(CosineAlgorithm(vec_type="tfidf"))
    # Compare files
    alt_path = get_user_input("Enter the path to directory containing the files to compare (q to exit): ")
    if alt_path:
        mediator.run_comparison(show_ground_truth=True)
    else:
        print("No valid path provided. Exiting...")
        exit()
