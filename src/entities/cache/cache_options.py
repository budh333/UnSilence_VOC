from typing import List
from enums.configuration import Configuration


class CacheOptions:
    def __init__(
            self,
            item_key: str,
            configuration_specific: bool = True,
            language_specific: bool = True,
            challenge_specific: bool = True,
            seed_specific: bool = False,
            configuration: Configuration = None,
            seed: int = None,
            key_suffixes: List[str] = None):

        self._item_key = item_key
        self._configuration_specific = configuration_specific
        self._language_specific = language_specific
        self._challenge_specific = challenge_specific
        self._seed_specific = seed_specific
        self._configuration = configuration
        self._seed = seed
        self._key_suffixes = key_suffixes

    def get_item_key(self) -> str:
        result = self._item_key
        if self._key_suffixes is not None:
            for key_suffix in self._key_suffixes:
                result += key_suffix

        return result

    @property
    def configuration_specific(self) -> bool:
        return self._configuration_specific

    @property
    def language_specific(self) -> bool:
        return self._language_specific

    @property
    def challenge_specific(self) -> bool:
        return self._challenge_specific

    @property
    def seed_specific(self) -> bool:
        return self._seed_specific

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    @property
    def seed(self) -> int:
        return self._seed
