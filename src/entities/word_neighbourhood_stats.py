from typing import List
from entities.word_evaluation import WordEvaluation

class WordNeighbourhoodStats:
    def __init__(
            self,
            target_word: str,
            neighbourhoods: List[List[WordEvaluation]]):

        self._target_word = target_word
        self._neighbourhoods = neighbourhoods

        self._overlapping_words = self._calculate_overlaps()

    def _calculate_overlaps(self) -> List[str]:
        if self.neighbourhoods_amount < 2:
            return []

        overlaps = set(self._neighbourhoods[0])
        for neighbourhood in self._neighbourhoods[1:]:
            overlaps = overlaps & set(neighbourhood)

        result = len(overlaps)
        return result

    def add_neighbourhood(self, neighbourhood: List[WordEvaluation]):
        self._neighbourhoods.append(neighbourhood)
        self._overlapping_words = self._calculate_overlaps()

    def get_all_embeddings(self) -> List[List[float]]:
        result = []
        for i, neighbourhood in enumerate(self._neighbourhoods):
            for word_evaluation in neighbourhood:
                result.append(word_evaluation.get_embeddings(i))

        return result

    def get_all_words(self) -> List[str]:
        result = []
        for neighbourhood in self._neighbourhoods:
            for word_evaluation in neighbourhood:
                result.append(word_evaluation.word)

        return result

    @property
    def target_word(self) -> str:
        return self._target_word

    @property
    def overlaps_amount(self) -> int:
        return self._overlapping_words

    @property
    def neighbourhoods_amount(self) -> int:
        return len(self._neighbourhoods)

    @property
    def neighbourhood_size(self) -> int:
        return len(self._neighbourhoods[0])

