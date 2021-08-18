
from typing import List


class TokenRepresentation:
    def __init__(self, token: str, vocabulary_ids: List[List[int]]):
        self._token = token
        self._vocabulary_ids = vocabulary_ids

    @property
    def token(self) -> str:
        return self._token

    @property
    def vocabulary_ids(self) -> List[List[int]]:
        return self._vocabulary_ids