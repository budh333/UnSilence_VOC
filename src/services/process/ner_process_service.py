from enums.run_type import RunType
from entities.ner.ne_line import NELine
from enums.language import Language
from entities.ner.ne_collection import NECollection
import os
import csv
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

        challenge_path = file_service.get_challenge_path()
        language_suffix = self._get_language_suffix(arguments_service.language)

        train_cache_key = f'train-data-limit-{arguments_service.train_dataset_limit_size}-merge-{arguments_service.merge_subwords}-replacen-{arguments_service.replace_all_numbers}'
        validation_cache_key = f'validation-data-limit-{arguments_service.validation_dataset_limit_size}-merge-{arguments_service.merge_subwords}-replacen-{arguments_service.replace_all_numbers}'
        self._train_ne_collection = cache_service.get_item_from_cache(
            CacheOptions(
                item_key=train_cache_key,
                configuration_specific=False),
            callback_function=lambda: (
                self.preprocess_data(
                    os.path.join(
                        challenge_path, f'data-train-{language_suffix}.tsv'),
                    limit=arguments_service.train_dataset_limit_size)))

        self._validation_ne_collection = cache_service.get_item_from_cache(
            CacheOptions(
                item_key=validation_cache_key,
                configuration_specific=False),
            callback_function=lambda: (
                self.preprocess_data(
                    os.path.join(
                        challenge_path, f'data-dev-{language_suffix}.tsv'),
                    limit=arguments_service.validation_dataset_limit_size)))

        self._entity_mappings = self._create_entity_mappings(
            self._train_ne_collection,
            self._validation_ne_collection)

        vocabulary_cache_key = f'char-vocabulary'
        vocabulary_data = cache_service.get_item_from_cache(
            CacheOptions(item_key=vocabulary_cache_key),
            callback_function=lambda: self._generate_vocabulary_data(language_suffix))

        vocabulary_service.initialize_vocabulary_data(vocabulary_data)

    def preprocess_data(
            self,
            file_path: str,
            limit: int = None) -> NECollection:
        if not os.path.exists(file_path):
            raise Exception(f'NER File not found at "{file_path}"')

        collection = NECollection()

        with open(file_path, 'r', encoding='utf-8') as tsv_file:
            reader = csv.DictReader(
                tsv_file, dialect=csv.excel_tab, quoting=csv.QUOTE_NONE)
            current_sentence = NELine()

            for row in reader:
                if row['TOKEN'] == '':
                    continue

                is_new_document = row['TOKEN'].startswith('# document')
                is_comment = row['TOKEN'].startswith('#')

                document_id = None
                if is_new_document:
                    document_id = row['TOKEN'].split('=')[-1].strip()

                    if len(current_sentence.tokens) == 0:
                        current_sentence.document_id = document_id

                if is_new_document:
                    if len(current_sentence.tokens) > 0:
                        current_sentence.tokenize_text(
                            self._tokenize_service,
                            self._string_process_service,
                            replace_all_numbers=self._arguments_service.replace_all_numbers,
                            expand_targets=not self._arguments_service.merge_subwords)

                        collection.add_line(current_sentence)

                        current_sentence = NELine()
                        if document_id is not None:
                            current_sentence.document_id = document_id

                        if limit and len(collection) >= limit:
                            break
                elif is_comment:
                    continue
                else:
                    current_sentence.add_data(self._string_process_service, row, self._entity_tag_types)

        # add last document
        if len(current_sentence.tokens) > 0:
            current_sentence.tokenize_text(
                self._tokenize_service,
                self._string_process_service,
                replace_all_numbers=self._arguments_service.replace_all_numbers,
                expand_targets=not self._arguments_service.merge_subwords)

            collection.add_line(current_sentence)

        return collection

    def get_processed_data(self, run_type: RunType):
        if run_type == RunType.Train:
            return self._train_ne_collection
        elif run_type == RunType.Validation:
            return self._validation_ne_collection
        elif run_type == RunType.Test:
            if not self._arguments_service.evaluate:
                raise Exception(
                    'You must have an evaluation run to use test collection')
            return self._test_ne_collection

        raise Exception('Unsupported run type')

    def get_main_entities(self, entity_tag_type: EntityTagType) -> set:
        entity_mapping_keys = [
            key for key, value in self._entity_mappings[entity_tag_type].items() if value >= 4]
        entities = set([x[2:] for x in entity_mapping_keys if x[2:] != ''])
        return entities

    def get_labels_amount(self) -> Dict[EntityTagType, int]:
        result = {
            entity_tag_type: len(entity_mapping) for entity_tag_type, entity_mapping in self._entity_mappings.items()
        }

        return result

    def get_entity_labels(self, ne_line: NELine, ignore_unknown: bool = False) -> List[int]:
        labels = {
            entity_tag_type: None for entity_tag_type in self._entity_tag_types
        }

        for entity_tag_type in self._entity_tag_types:
            current_entity_tags = ne_line.get_entity_tags(entity_tag_type)
            labels[entity_tag_type] = [
                self.get_entity_label(entity, entity_tag_type, ignore_unknown=ignore_unknown) for entity in current_entity_tags
            ]

        return labels

    def get_entity_label(self, entity_tag: str, entity_tag_type: EntityTagType, ignore_unknown: bool = False) -> int:
        if entity_tag_type not in self._entity_mappings.keys():
            raise Exception(f'Invalid entity tag type - "{entity_tag_type}"')

        if entity_tag not in self._entity_mappings[entity_tag_type].keys():
            if ignore_unknown:
                return self._entity_mappings[entity_tag_type]['O']

            raise Exception(f'Invalid entity tag - "{entity_tag}"')

        return self._entity_mappings[entity_tag_type][entity_tag]

    def get_entity_by_label(self, label: int, entity_tag_type: EntityTagType, ignore_unknown: bool = False) -> str:
        if entity_tag_type not in self._entity_mappings.keys():
            raise Exception('Invalid entity tag type')

        for entity, entity_label in self._entity_mappings[entity_tag_type].items():
            if label == entity_label:
                return entity

        if ignore_unknown:
            return 'O'

        raise Exception('Entity not found for this label')

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

    def _generate_vocabulary_data(self, language_suffix: str):
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
            'id2token': int2char,
            'token2id': char2int
        }

        return vocabulary_data

    def _get_language_suffix(self, language: Language):
        if language == Language.Dutch:
            return 'nl'
        else:
            raise Exception('Unsupported language')
