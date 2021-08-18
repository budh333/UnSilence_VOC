from typing import List

class Word2VecEntry:
    def __init__(self, document_idx: int, target_token: int, context_tokens: List[int]):
        if len(context_tokens) == 0:
            raise Exception('Context tokens not supplied')

        self._document_idx = document_idx
        self._target_token = target_token
        self._context_tokens = context_tokens

    def __repr__(self):
        context_words_string = "','".join(self._context_tokens)
        return f'target: \'{self._target_token}\' | context: \'{context_words_string}\''

    @property
    def document_index(self) -> int:
        return self._document_idx

    @property
    def target_token(self) -> int:
        return self._target_token

    @property
    def context_tokens(self) -> List[int]:
        return self._context_tokens