from enums.language import Language
from entities.ner.ne_collection import NECollection
import os
from services.data_service import DataService
from services.file_service import FileService
from services.arguments.ner_arguments_service import NERArgumentsService
from enums.entity_tag_type import EntityTagType
from entities.cache.cache_options import CacheOptions
from typing import Dict, List, Tuple
import random

from enums.ocr_output_type import OCROutputType

from entities.transformers.transformer_entry import TransformerEntry

from services.process.process_service_base import ProcessServiceBase
from services.tokenize.base_tokenize_service import BaseTokenizeService

from services.vocabulary_service import VocabularyService
from services.cache_service import CacheService
from services.log_service import LogService
from services.string_process_service import StringProcessService


class NERProcessService(ProcessServiceBase):
    def __init__(
            self,
            arguments_service: NERArgumentsService,
            vocabulary_service: VocabularyService,
            file_service: FileService,
            tokenize_service: BaseTokenizeService,
            data_service: DataService,
            cache_service: CacheService,
            string_process_service: StringProcessService):
        self._arguments_service = arguments_service
        self._tokenize_service = tokenize_service
        self._file_service = file_service
        self._data_service = data_service
        self._string_process_service = string_process_service

        self._entity_tag_types = arguments_service.entity_tag_types

        self.PAD_TOKEN = '[PAD]'
        self.START_TOKEN = '[CLS]'
        self.STOP_TOKEN = '[SEP]'

        self.pad_idx = 0
        self.start_idx = 1
        self.stop_idx = 2

        data_path = file_service.get_data_path()
        language_suffix = self._get_language_suffix(arguments_service.language)

        train_cache_key = f'train-hipe-data-limit-{arguments_service.train_dataset_limit_size}-merge-{arguments_service.merge_subwords}-replacen-{arguments_service.replace_all_numbers}'
        validation_cache_key = f'validation-hipe-data-limit-{arguments_service.validation_dataset_limit_size}-merge-{arguments_service.merge_subwords}-replacen-{arguments_service.replace_all_numbers}'
        self._train_ne_collection = cache_service.get_item_from_cache(
            CacheOptions(item_key=train_cache_key),
            callback_function=lambda: (
                self.preprocess_data(
                    os.path.join(
                        data_path, f'HIPE-data-train-{language_suffix}.tsv'),
                    limit=arguments_service.train_dataset_limit_size)))

        self._validation_ne_collection = cache_service.get_item_from_cache(
            CacheOptions(item_key=validation_cache_key),
            callback_function=lambda: (
                self.preprocess_data(
                    os.path.join(
                        data_path, f'HIPE-data-dev-{language_suffix}.tsv'),
                    limit=arguments_service.validation_dataset_limit_size)))

        self._entity_mappings = self._create_entity_mappings(
            self._train_ne_collection,
            self._validation_ne_collection)

        vocabulary_cache_key = f'char-vocabulary-{self._data_version}'
        vocabulary_data = cache_service.get_item_from_cache(
            CacheOptions(item_key=vocabulary_cache_key),
            callback_function=lambda: self._generate_vocabulary_data(language_suffix, self._data_version))

        vocabulary_service.initialize_vocabulary_data(vocabulary_data)

    def preprocess_data(
            self,
            file_path: str,
            limit: int = None) -> NECollection:
        if not os.path.exists(file_path):
            raise Exception(f'NER File not found at "{file_path}"')

    def get_labels_amount(self) -> Dict[EntityTagType, int]:
        result = {
            entity_tag_type: len(entity_mapping) for entity_tag_type, entity_mapping in self._entity_mappings.items()
        }

        return result

    def _create_entity_mappings(
            self,
            train_ne_collection: NECollection,
            validation_ne_collection: NECollection) -> Dict[EntityTagType, Dict[str, int]]:

        entity_mappings = {
            entity_tag_type: None for entity_tag_type in self._entity_tag_types
        }

        for entity_tag_type in self._entity_tag_types:
            entities = train_ne_collection.get_unique_entity_tags(
                entity_tag_type)
            entities.extend(
                validation_ne_collection.get_unique_entity_tags(entity_tag_type))
            entities = list(set(entities))
            entities.sort(key=lambda x: '' if x is None else x)
            entity_mapping = {x: i+3 for i, x in enumerate(entities)}
            entity_mapping[self.PAD_TOKEN] = self.pad_idx
            entity_mapping[self.START_TOKEN] = self.start_idx
            entity_mapping[self.STOP_TOKEN] = self.stop_idx

            entity_mappings[entity_tag_type] = entity_mapping

        return entity_mappings

    def _generate_vocabulary_data(self, language_suffix: str, data_version: str):
        unique_characters = set()

        for ne_line in self._train_ne_collection.lines:
            current_unique_characters = set(
                [char for token in ne_line.tokens for char in token])
            unique_characters = unique_characters.union(
                current_unique_characters)

        for ne_line in self._validation_ne_collection.lines:
            current_unique_characters = set(
                [char for token in ne_line.tokens for char in token])
            unique_characters = unique_characters.union(
                current_unique_characters)

        unique_characters = sorted(list(unique_characters))
        unique_characters.insert(0, '[PAD]')
        unique_characters.insert(1, '[UNK]')
        unique_characters.insert(2, '[CLS]')
        unique_characters.insert(3, '[EOS]')

        int2char = dict(enumerate(unique_characters))
        char2int = {char: index for index, char in int2char.items()}
        vocabulary_data = {
            'characters-set': unique_characters,
            'int2char': int2char,
            'char2int': char2int
        }

        return vocabulary_data

    def _get_language_suffix(self, language: Language):
        if language == Language.Dutch:
            return 'nl'
        else:
            raise Exception('Unsupported language')
