from typing import List

class TransformerEntry:
    def __init__(self, document_idx: int, token_ids: List[int], mask_ids: List[int]):
        self._document_idx = document_idx
        self._token_ids = token_ids
        self._mask_ids = mask_ids

    @property
    def document_index(self) -> int:
        return self._document_idx

    @property
    def token_ids(self) -> List[int]:
        return self._token_ids

    @property
    def mask_ids(self) -> List[int]:
        return self._mask_ids