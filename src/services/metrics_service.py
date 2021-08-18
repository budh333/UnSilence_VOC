import jellyfish
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, precision_recall_fscore_support
import scipy.spatial.distance as scipy_distances
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity

from typing import Tuple


class MetricsService:
    def __init__(self):
        pass

    def calculate_jaccard_similarity(self, list1: list, list2: list) -> float:
        if len(list1) == 0 and len(list2) == 0:
            return 0

        set1 = set(list1)
        set2 = set(list2)
        return len(set1.intersection(set2)) / len(set1.union(set2))

    def calculate_normalized_levenshtein_distance(self, string1: str, string2: str) -> int:
        """Calculates normalized levenshtein distance between two strings

        :param string1: first string to be used
        :type string1: str
        :param string2: second string to be used
        :type string2: str
        :return: the normalized levenshtein distance integer
        :rtype: int
        """
        result = float(self.calculate_levenshtein_distance(
            string1, string2)) / max(len(string1), len(string2))

        return result

    def calculate_levenshtein_distance(self, string1: str, string2: str) -> int:
        """Calculates levenshtein distance, unnormalized

        :param string1: first string to be used
        :type string1: str
        :param string2: second string to be used
        :type string2: str
        :return: the levenshtein distance integer
        :rtype: int
        """
        result = jellyfish.levenshtein_distance(string1, string2)
        return result

    def calculate_f1_score(
            self,
            predictions,
            targets) -> float:
        """Calculates F1 score between predicted values and original ground-truth targets

        :param predictions: Predicted values
        :type predictions: Any
        :param targets: Target values
        :type targets: Any
        :return: F1 score float number
        :rtype: float
        """
        result = f1_score(targets, predictions)
        return result

    def calculate_precision_score(
            self,
            predictions,
            targets) -> float:
        """Calculates precision score between predicted values and original ground-truth targets

        :param predictions: Predicted values
        :type predictions: Any
        :param targets: Target values
        :type targets: Any
        :return: Precision score float number
        :rtype: float
        """
        result = precision_score(targets, predictions)
        return result

    def calculate_recall_score(
            self,
            predictions,
            targets) -> float:
        """Calculates recall score between predicted values and original ground-truth targets

        :param predictions: Predicted values
        :type predictions: Any
        :param targets: Target values
        :type targets: Any
        :return: Recall score float number
        :rtype: float
        """
        result = recall_score(targets, predictions)
        return result

    def calculate_precision_recall_fscore_support(
            self,
            predictions,
            targets) -> Tuple[float, float, float, float]:
        """Calculates precision, recall and F1 scores between predicted values and original ground-truth targets

        :param predictions: Predicted values
        :type predictions: Any
        :param targets: Target values
        :type targets: Any
        :return: Precision, recall and F1 scores float numbers
        :rtype: float
        """
        result = precision_recall_fscore_support(
            targets,
            predictions,
            warn_for=tuple())

        return result

    def calculate_cosine_distance(self, list1: list, list2: list) -> float:
        """Calculates the cosine distance between two lists of numbers

        :param list1: First list of numbers
        :type list1: list
        :param list2: Second list of numbers
        :type list2: list
        :return: The cosine distance
        :rtype: float
        """
        if np.sum(list1) == 0 or np.sum(list2) == 0:
            return 0

        cosine_distance = scipy_distances.cosine(list1, list2)
        return cosine_distance

    def calculate_euclidean_distance(self, list1: list, list2: list) -> float:
        """Calculates the euclidean distance between two lists of numbers

        :param list1: First list of numbers
        :type list1: list
        :param list2: Second list of numbers
        :type list2: list
        :return: The euclidean distance
        :rtype: float
        """
        euclidean_distance = scipy_distances.euclidean(list1, list2)
        return euclidean_distance

    def calculate_cosine_similarity(self, list1: list, list2: list) -> float:
        """
        Calculates cosine similarity using scipy cosine distance.

        Original formula is `cosine_distance = 1 - cosine_similarity`.
        Thus `cosine_similarity = cosine_distance + 1`

        Results are to be described as
        - −1 meaning exactly opposite
        - +1 meaning exactly the same
        - 0 indicating orthogonality
        """

        cosine_distance = scipy_distances.cosine(list1, list2)
        return cosine_distance - 1


    def calculate_cosine_similarities(self, matrix1: np.ndarray, matrix2: np.ndarray) -> float:
        """
        Calculates cosine similarity using scipy cosine distance.

        Original formula is `cosine_distance = 1 - cosine_similarity`.
        Thus `cosine_similarity = cosine_distance + 1`

        Results are to be described as
        - −1 meaning exactly opposite
        - +1 meaning exactly the same
        - 0 indicating orthogonality
        """

        cosine_distance = cosine_similarity(matrix1, matrix2)
        return cosine_distance
