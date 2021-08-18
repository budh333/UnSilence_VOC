from typing import List
from overrides import overrides

import argparse

from services.arguments.pretrained_arguments_service import PretrainedArgumentsService

from enums.entity_tag_type import EntityTagType
# from enums.text_sequence_split_type import TextSequenceSplitType


class NERArgumentsService(PretrainedArgumentsService):
    def __init__(self):
        super().__init__()

    @overrides
    def get_configuration_name(self) -> str:
        pass

    @overrides
    def _add_specific_arguments(self, parser: argparse.ArgumentParser):
        super()._add_specific_arguments(parser)

        parser.add_argument('--entity-tag-types', type=EntityTagType, choices=list(EntityTagType), default=EntityTagType.Main, nargs='*',
                            help='Entity tag types that will be used for classification. Default is to only use `Main`')
        parser.add_argument("--merge-subwords", action='store_true',
                            help="whether to merge the subword embeddings before passing through the RNN")
        parser.add_argument("--replace-all-numbers", action='store_true',
                            help="If all numbers should be replaced by a hard-coded fixed string")


    @property
    def entity_tag_types(self) -> List[EntityTagType]:
        return self._get_argument('entity_tag_types')

    @property
    def merge_subwords(self) -> bool:
        return self._get_argument('merge_subwords')

    @property
    def replace_all_numbers(self) -> int:
        return self._get_argument('replace_all_numbers')