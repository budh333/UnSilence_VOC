from enums.overlap_type import OverlapType
from typing import List

class WordEvaluation:
    def __init__(self, word: str, embeddings_list: List[List[List[float]]] = None):
        self._word = word
        self._embeddings = embeddings_list

    def add_embeddings(self, embeddings: List[int], idx: int):
        if self._embeddings is None:
            self._embeddings = []

        # make sure the list is big enough
        while len(self._embeddings) <= idx:
            self._embeddings.append(None)

        if embeddings is not None:
            self._embeddings[idx] = embeddings

    def get_embeddings(self, idx: int) -> list:
        if idx > len(self._embeddings):
            raise Exception('Invalid embeddings index')

        return self._embeddings[idx]

    def get_embeddings_size(self) -> int:
        filled_embeddings = list(filter(lambda x: x is not None, self._embeddings))
        if len(filled_embeddings) == 0:
            return None

        return len(filled_embeddings[0])

    @property
    def word(self) -> str:
        return self._word

    def contains_embeddings(self, embeddings_idx: int) -> bool:
        return self._embeddings[embeddings_idx] is not None

    def contains_all_embeddings(self, overlap_type: OverlapType = None) -> bool:
        if overlap_type is None:
            result = len(self._embeddings) >= 3 and all([x is not None for x in self._embeddings])
            return result

        # result = len(self._embeddings) >= 3 and self._embeddings[2] is not None
        result = True
        if overlap_type != OverlapType.GTvsOCR:
            result = len(self._embeddings) >= 3 and self._embeddings[2] is not None

        if overlap_type == OverlapType.BASEvsGT:
            return (result and self._embeddings[1] is not None)
        elif overlap_type == OverlapType.BASEvsOCR:
            return (result and self._embeddings[2] is not None)
        elif overlap_type == OverlapType.BASEvsOG:
            return (result and len(self._embeddings) >= 4 and self._embeddings[3] is not None)
        elif overlap_type == OverlapType.GTvsOCR:
            return (result and self._embeddings[1] is not None and self._embeddings[0] is not None)

        raise NotImplementedError(f'Overlap type {overlap_type.value} is not implemented')

    def __str__(self):
        return self._word
