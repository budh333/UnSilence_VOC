from enums.configuration import Configuration
from entities.cache.cache_options import CacheOptions
import os
from services.log_service import LogService
from typing import Counter, List, Dict, Tuple

import nltk
from nltk.corpus import wordnet as wn
from numpy.core.numeric import full
from numpy.lib.arraysetops import unique

from services.arguments.arguments_service_base import ArgumentsServiceBase
from services.data_service import DataService
from services.file_service import FileService
from services.cache_service import CacheService


class VocabularyService:
    def __init__(
            self,
            data_service: DataService,
            file_service: FileService,
            cache_service: CacheService,
            log_service: LogService,
            overwrite_configuration: Configuration = None):

        self._data_service = data_service
        self._file_service = file_service
        self._cache_service = cache_service
        self._log_service = log_service

        self._vocabulary_cache_key = 'vocab'
        self._overwrite_configuration = overwrite_configuration

        self._id2token: Dict[int, str] = {}
        self._token2idx: Dict[str, int] = {}

        self.load_cached_vocabulary(self._vocabulary_cache_key)

    def load_cached_vocabulary(self, cache_key: str) -> bool:
        """Load vocabulary from a cached value

        :param cache_key: The cache key to be used for the vocabulary file
        :type cache_key: str
        :return: Whether the loading was successful. If the vocabulary file does not exist, then False will be returned
        :rtype: bool
        """
        cache_options = CacheOptions(
            cache_key,
            configuration=self._overwrite_configuration)

        self._vocabulary_cache_key = cache_key

        cached_vocabulary_exists = self._cache_service.item_exists(
            cache_options)
        if cached_vocabulary_exists:
            cached_vocabulary = self._cache_service.get_item_from_cache(
                cache_options)
            if cached_vocabulary is not None:
                self._log_service.log_debug('Cached vocabulary found')
                (self._token2idx, self._id2token) = cached_vocabulary
                return self.vocabulary_is_initialized()

        self._log_service.log_warning('Cached vocabulary was not found')
        return False

    def initialize_vocabulary_data(self, vocabulary_data: dict):
        """Initialize vocabulary from vocabulary data

        :param vocabulary_data: Dictionary containing 'id2token' and 'token2id' entries
        :type vocabulary_data: dict
        """
        if vocabulary_data is None:
            return

        self._id2token: Dict[int, str] = vocabulary_data['id2token']
        self._token2idx: Dict[str, int] = vocabulary_data['token2id']

        self._log_service.log_debug('Initialized vocabulary data')

    def string_to_ids(self, input: List[str]) -> List[int]:
        """Convert list of string tokens to vocabulary ids

        :param input: List of string tokens
        :type input: List[str]
        :return: List of integer values, the vocabulary ids
        :rtype: List[int]
        """
        result = [self.string_to_id(x) for x in input]
        return result

    def string_to_id(self, input: str) -> int:
        """Convert one string token to a vocabulary id

        :param input: The string token
        :type input: str
        :return: Vocabulary id or UNK token id if the token is not part of the vocabulary
        :rtype: int
        """
        if input in self._token2idx.keys():
            return self._token2idx[input]

        return self.unk_token

    def ids_to_string(
            self,
            input: List[int],
            exclude_special_tokens: bool = True,
            join_str: str = '',
            cut_after_end_token: bool = False) -> str:
        """Convert list of vocabulary ids to a string

        :param input: List of integer values, vocabulary ids
        :type input: List[int]
        :param exclude_special_tokens: If True, all special tokens such as PAD, UNK will be excluded from the string result, defaults to True
        :type exclude_special_tokens: bool, optional
        :param join_str: The value that will be used to concatenate the string tokens, defaults to ''
        :type join_str: str, optional
        :param cut_after_end_token: If True, the result will be cut after the first EOS encountered token, defaults to False
        :type cut_after_end_token: bool, optional
        :raises Exception: If join_str is invalid value or not a string
        :return: The concatenated string
        :rtype: str
        """
        if join_str is None:
            raise Exception('`join_str` must be a valid string')

        result = join_str.join([self._id2token[x] for x in input])

        if cut_after_end_token:
            try:
                eos_index = result.index('[EOS]')
                result = result[:eos_index]
            except ValueError:
                pass

        if exclude_special_tokens:
            result = result.replace('[PAD]', '')
            result = result.replace('[EOS]', '')
            result = result.replace('[CLS]', '')

        return result

    def ids_to_strings(
            self,
            input: List[int],
            exclude_pad_tokens: bool = True) -> List[str]:
        """Convert list of vocabulary ids to a list of their string token equivalents

        :param input: List of vocabulary integer ids
        :type input: List[int]
        :param exclude_pad_tokens: If true, padding tokens will be excluded from the end result, defaults to True
        :type exclude_pad_tokens: bool, optional
        :return: List of string tokens converted from the ids
        :rtype: List[str]
        """
        result = [self._id2token[x] for x in input]

        if exclude_pad_tokens:
            result = list(filter(lambda x: x != '[PAD]', result))

        return result

    def vocabulary_size(self) -> int:
        return len(self._id2token)

    def get_vocabulary_tokens(self, exclude_special_tokens: bool = False) -> List[Tuple[int, str]]:
        """Get all tokens part of the vocabulary

        :param exclude_special_tokens: If true, special tokens will be excluded from the result, defaults to False
        :type exclude_special_tokens: bool, optional
        :return: List of Tuples in (id, token) format
        :rtype: List[Tuple[int, str]]
        """
        for index, token in self._id2token.items():
            if exclude_special_tokens and index < 4:
                continue

            yield (index, token)

    def initialize_vocabulary_from_corpus(
            self,
            tokenized_corpus: List[List[str]],
            min_occurrence_limit: int = None,
            vocab_key: str = None):
        """Initialize the vocabulary from a list of tokenized sentences

        :param tokenized_corpus: List of lists of string tokens
        :type tokenized_corpus: List[List[str]]
        :param min_occurrence_limit: Optional minimal occurrence limit. All tokens that occur less than this amount will not be saved to the vocabulary. 
        If None is used, all tokens will be used, defaults to None
        :type min_occurrence_limit: int, optional
        :param vocab_key: Key to name the vocabulary and cache it, defaults to None
        :type vocab_key: str, optional
        """
        if len(self._token2idx) > 0 and len(self._id2token) > 0:
            return

        unique_tokens = list(
            set([token for sentence in tokenized_corpus for token in sentence]))

        if min_occurrence_limit is not None:
            unique_tokens = self._filter_tokens_by_occurrence(
                tokenized_corpus, unique_tokens, min_occurrence_limit)

        unique_tokens = list(sorted(unique_tokens))
        vocabulary = [
            '[PAD]',
            '[CLS]',
            '[EOS]',
            '[UNK]'
        ]

        vocabulary.extend(unique_tokens)

        self._token2idx = {w: idx for (idx, w) in enumerate(vocabulary)}
        self._id2token = {idx: w for (idx, w) in enumerate(vocabulary)}

        if vocab_key is None:
            vocab_key = self._vocabulary_cache_key
        self._cache_vocabulary(vocab_key)

    def vocabulary_is_initialized(self) -> bool:
        """Check if the vocabulary has been initialized

        :return: True if the vocabulary is initialized, otherwise False
        :rtype: bool
        """
        return self._id2token is not None and len(self._id2token) > 0 and self._token2idx is not None and len(self._token2idx) > 0

    def token_exists(self, token: str) -> bool:
        """Check if a token is part of the vocabulary

        :param token: Token to be checked
        :type token: str
        :return: True if the token is part of the vocabulary
        :rtype: bool
        """
        result = (token in self._token2idx.keys())
        return result

    def _filter_tokens_by_occurrence(self, full_corpus: List[List[str]], unique_tokens: List[str], min_occurrence_limit: int) -> List[str]:
        all_tokens = [inner for outer in full_corpus for inner in outer]
        tokens_counter = Counter(all_tokens)
        limit_tokens = [
            token for token in unique_tokens if tokens_counter[token] > min_occurrence_limit]
        return limit_tokens

    def _cache_vocabulary(self, vocab_key: str):
        self._cache_service.cache_item(
            [
                self._token2idx,
                self._id2token
            ],
            CacheOptions(
                vocab_key, configuration=self._overwrite_configuration),
            overwrite=False)

    @property
    def cls_token(self) -> int:
        return self._token2idx['[CLS]']

    @property
    def eos_token(self) -> int:
        return self._token2idx['[EOS]']

    @property
    def unk_token(self) -> int:
        return self._token2idx['[UNK]']

    @property
    def pad_token(self) -> int:
        return self._token2idx['[PAD]']
