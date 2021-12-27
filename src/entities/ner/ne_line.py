from typing import Dict, List
from copy import deepcopy
import re

from enums.entity_tag_type import EntityTagType
from enums.word_feature import WordFeature
from services.tokenize.base_tokenize_service import BaseTokenizeService
from services.string_process_service import StringProcessService


class NELine:
    def __init__(self):
        self.tokens: List[str] = []
        self.tokens_features: List[List[int]] = []
        self.token_ids = []
        self.misc = []
        self.ne_main = []
        self.ne_person_name = []
        self.ne_person_gender = []
        self.ne_person_legal_status = []
        self.ne_person_role = []

        self.original_length = 0
        self.position_changes: Dict[int, List[int]] = None

        self.document_id = None

    def add_data(
            self,
            string_process_service: StringProcessService,
            csv_row: dict,
            possible_entity_tag_types: List[EntityTagType]):
        clean_up_tokens = True
        if clean_up_tokens:
            token = string_process_service._clean_up_word(csv_row['TOKEN'])
            if token == '':
                return

        token = self._add_entity_if_available(csv_row, 'TOKEN', self.tokens)

        self.tokens_features.append(self._get_token_features(token))

        self._add_entity_if_available(
            csv_row, 'MISC', self.misc, use_none_if_empty=True)

        if EntityTagType.Main in possible_entity_tag_types:
            self._add_entity_if_available(
                csv_row, 'NE-MAIN', self.ne_main, use_none_if_empty=True)

        if EntityTagType.Name in possible_entity_tag_types:
            self._add_entity_if_available(
                csv_row, 'NE-PER-NAME', self.ne_person_name, use_none_if_empty=True)

        if EntityTagType.Gender in possible_entity_tag_types:
            self._add_entity_if_available(
                csv_row, 'NE-PER-GENDER', self.ne_person_gender, use_none_if_empty=True)

        if EntityTagType.LegalStatus in possible_entity_tag_types:
            self._add_entity_if_available(
                csv_row, 'NE-PER-LEGAL-STATUS', self.ne_person_legal_status, use_none_if_empty=True)

        if EntityTagType.Role in possible_entity_tag_types:
            self._add_entity_if_available(
                csv_row, 'NE-PER-ROLE', self.ne_person_role, use_none_if_empty=True)

    def _get_token_features(self, token: str) -> Dict[WordFeature, bool]:
        result = {
            WordFeature.AllLower: self._get_feature_value(token.islower(), WordFeature.AllLower),
            WordFeature.AllUpper: self._get_feature_value(token.isupper(), WordFeature.AllUpper),
            WordFeature.IsTitle: self._get_feature_value(token.istitle(), WordFeature.IsTitle),
            WordFeature.FirstLetterUpper: self._get_feature_value(token[0].isupper(), WordFeature.FirstLetterUpper),
            WordFeature.FirstLetterNotUpper: self._get_feature_value(not token[0].isupper(), WordFeature.FirstLetterNotUpper),
            WordFeature.Numeric: self._get_feature_value(token.isdigit(), WordFeature.Numeric),
            WordFeature.NoAlphaNumeric: self._get_feature_value(not token.isalnum(), WordFeature.NoAlphaNumeric),
        }

        return result

    def _get_feature_value(self, feature: bool, feature_type: WordFeature):
        if feature:
            return feature_type.value
        else:
            return feature_type.value + len(WordFeature)

    def _insert_entity_tag(self, list_to_modify: list, position: int, tag: str):
        tag_to_insert = tag
        if tag.startswith('B-'):
            tag_to_insert = f'I-{tag[2:]}'

        list_to_modify.insert(position, tag_to_insert)

    def get_entity_tags(self, entity_tag_type: EntityTagType):
        if entity_tag_type == EntityTagType.Main:
            return self.ne_main
        if entity_tag_type == EntityTagType.Name:
            return self.ne_person_name
        elif entity_tag_type == EntityTagType.Gender:
            return self.ne_person_gender
        elif entity_tag_type == EntityTagType.LegalStatus:
            return self.ne_person_legal_status
        elif entity_tag_type == EntityTagType.Role:
            return self.ne_person_role
        else:
            raise Exception(f'Unsupported entity tag type {entity_tag_type}')

    def tokenize_text(
            self,
            tokenize_service: BaseTokenizeService,
            string_process_service: StringProcessService,
            replace_all_numbers: bool = False,
            expand_targets: bool = True):
        if replace_all_numbers:
            self.tokens = string_process_service.replace_strings_numbers(
                self.tokens)

        self.original_length = len(self.tokens)
        text = self.get_text()
        offsets = self.get_token_offsets()

        token_ids, encoded_tokens, encoded_offsets, _ = tokenize_service.encode_sequence(
            text)

        # it means that the tokenizer has split some of the words, therefore we need to add
        # those tokens to our collection and repeat the entity labels for the new sub-tokens
        position_changes = {i: [i] for i in range(len(self.tokens))}
        if len(encoded_tokens) > len(self.tokens):
            new_misc = deepcopy(self.misc)
            new_tokens_features = deepcopy(self.tokens_features)
            new_ne_main = deepcopy(self.ne_main)
            new_ne_person_name = deepcopy(self.ne_person_name)
            new_ne_person_gender = deepcopy(self.ne_person_gender)
            new_ne_person_legal_status = deepcopy(self.ne_person_legal_status)
            new_ne_person_role = deepcopy(self.ne_person_role)

            position_changes = {}
            corresponding_counter = 0

            for i, token in enumerate(self.tokens):
                position_changes[i] = [corresponding_counter]

                while corresponding_counter < len(encoded_tokens) and encoded_offsets[corresponding_counter][1] < offsets[i][1]:

                    new_tokens_features.insert(
                        corresponding_counter+1, self.tokens_features[i])

                    # we always insert false for new segment start, since even if the current object is start of segment,
                    # expanding it should not make the segment start appear twice
                    if expand_targets:
                        # we copy the value of the original token
                        self._insert_entity_tag(
                            new_misc, corresponding_counter+1, self.misc[i])
                        self._insert_entity_tag(
                            new_ne_main, corresponding_counter+1, self.ne_main[i])
                        self._insert_entity_tag(
                            new_ne_person_name, corresponding_counter+1, self.ne_person_name[i])
                        self._insert_entity_tag(
                            new_ne_person_gender, corresponding_counter+1, self.ne_person_gender[i])
                        self._insert_entity_tag(
                            new_ne_person_legal_status, corresponding_counter+1, self.ne_person_legal_status[i])
                        self._insert_entity_tag(
                            new_ne_person_role, corresponding_counter+1, self.ne_person_role[i])

                    corresponding_counter += 1
                    position_changes[i].append(corresponding_counter)

                corresponding_counter += 1

            self.tokens_features = new_tokens_features
            self.misc = new_misc
            self.ne_main = new_ne_main
            self.ne_person_name = new_ne_person_name
            self.ne_person_gender = new_ne_person_gender
            self.ne_person_legal_status = new_ne_person_legal_status
            self.ne_person_role = new_ne_person_role

        self.position_changes = position_changes

        assert len(token_ids) == len(encoded_tokens)

        if expand_targets:
            assert len(token_ids) == len(self.ne_main)

        self.tokens = encoded_tokens

        self.token_ids = token_ids

    def get_text(self):
        text = ''

        for i, token in enumerate(self.tokens):
            if token.startswith('##'):
                text = text[:-1]
                text += token[2:]
            else:
                text += token

            # if 'NoSpaceAfter' not in self.misc[i] and 'EndOfLine' not in self.misc[i]:
            text += ' '

        return text

    def get_token_offsets(self):
        offsets = []

        last_end = 0

        for i, token in enumerate(self.tokens):
            current_start = last_end
            current_end = current_start + len(token)
            last_end += len(token)

            # if 'NoSpaceAfter' not in self.misc[i] and 'EndOfLine' not in self.misc[i]:
            last_end += 1

            offsets.append((current_start, current_end))

        return offsets

    def get_token_info(self, pos: int):
        return [
            self.tokens[pos],
            self.ne_main[pos],
            self.ne_person_name[pos],
            self.ne_person_gender[pos],
            self.ne_person_legal_status[pos],
            self.ne_person_role[pos],
        ]

    def _add_entity_if_available(self, csv_row: dict, key: str, obj: list, use_none_if_empty: bool = False):
        if key not in csv_row.keys():
            return None

        result = None
        if csv_row[key] == '':
            result = None
        else:
            result = csv_row[key]
            if key != 'TOKEN':
                result = result.split(',')[0]

        if result is not None or use_none_if_empty:
            obj.append(result)

        return result
