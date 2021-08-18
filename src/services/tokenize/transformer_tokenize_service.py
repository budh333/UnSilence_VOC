import os

from typing import Tuple, List

from overrides import overrides

import sentencepiece as spm

from transformers import PreTrainedTokenizerFast, XLNetTokenizerFast
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast

from enums.configuration import Configuration
from services.arguments.pretrained_arguments_service import PretrainedArgumentsService

from services.tokenize.base_tokenize_service import BaseTokenizeService

class TransformerTokenizeService(BaseTokenizeService):
    def __init__(
            self,
            arguments_service: PretrainedArgumentsService):
        super().__init__()

        pretrained_weights = arguments_service.pretrained_weights
        self._tokenizer: PreTrainedTokenizerFast = self._tokenizer_type.from_pretrained(pretrained_weights)

    @overrides
    def encode_tokens(self, tokens: List[str]) -> List[int]:
        result = self._tokenizer.convert_tokens_to_ids(tokens)
        return result

    @overrides
    def decode_tokens(self, character_ids: List[int]) -> List[str]:
        result = self._tokenizer.decode(character_ids)
        return result

    @overrides
    def decode_string(self, character_ids: List[int]) -> List[str]:
        result = self._tokenizer.decode(character_ids)
        return result

    @overrides
    def id_to_token(self, character_id: int) -> str:
        result = self._tokenizer.decode([character_id])
        return result

    @overrides
    def encode_sequence(self, sequence: str) -> Tuple[List[int], List[str], List[Tuple[int,int]], List[int]]:
        encoded_representations = self._tokenizer.encode_plus(sequence)
        if len(encoded_representations.encodings) > 1:
            raise Exception('More than one encoding found during `encode_plus` operation')

        encoded_representation = encoded_representations.encodings[0]
        return (
            encoded_representation.ids,
            encoded_representation.tokens,
            encoded_representation.offsets,
            encoded_representation.special_tokens_mask)

    @overrides
    def encode_sequences(self, sequences: List[str]) -> List[Tuple[List[int], List[str], List[Tuple[int,int]], List[int]]]:
        encoded_representations = self._tokenizer.encode_plus(sequences)
        return [(x.ids, x.tokens, x.offsets, x.special_tokens_mask) for x in encoded_representations]

    @property
    @overrides
    def vocabulary_size(self) -> int:
        return self._tokenizer.vocab_size

    @property
    @overrides
    def mask_token(self) -> str:
        return '<mask>'

    @property
    def _tokenizer_type(self) -> type:
        return PreTrainedTokenizerFast