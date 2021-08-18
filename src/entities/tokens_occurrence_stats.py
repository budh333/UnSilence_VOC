from typing import List
from scipy import sparse
import numpy as np

class TokensOccurrenceStats:
    def __init__(
        self, 
        sentences: List[List[int]],
        vocabulary_size: int):

        mutual_occurrences = np.zeros((vocabulary_size, vocabulary_size), dtype=np.int32)

        for sentence in sentences:
            for i in range(len(sentence)):

                if i > 0:
                    mutual_occurrences[sentence[i], sentence[i-1]] = mutual_occurrences[sentence[i], sentence[i-1]] + 1
                    mutual_occurrences[sentence[i-1], sentence[i]] = mutual_occurrences[sentence[i-1], sentence[i]] + 1

                if i < len(sentence) - 1:
                    mutual_occurrences[sentence[i], sentence[i+1]] = mutual_occurrences[sentence[i], sentence[i+1]] + 1
                    mutual_occurrences[sentence[i+1], sentence[i]] = mutual_occurrences[sentence[i+1], sentence[i]] + 1

        self._mutual_occurrences = sparse.dok_matrix(mutual_occurrences)

    @property
    def mutual_occurrences(self) -> sparse.dok_matrix:
        return self._mutual_occurrences