from typing import Dict, List
from overrides import overrides

import argparse

from services.arguments.pretrained_arguments_service import PretrainedArgumentsService

from enums.entity_tag_type import EntityTagType


class NERArgumentsService(PretrainedArgumentsService):
    def __init__(self):
        super().__init__()

    @overrides
    def get_configuration_name(self, overwrite_args: Dict[str, object] = None) -> str:
        result = super().get_configuration_name(overwrite_args)

        entity_tag_types = self._get_value_or_default(overwrite_args, 'entity_tag_types', self.entity_tag_types)
        entity_tag_types_str = f'-ett-{"-".join([self._cut_string(x.value) for x in entity_tag_types])}'
        result += entity_tag_types_str
        return result

    def _cut_string(self, text: str):
        spl_text = ''.join([x[0].lower() for x in text.split('-')])
        return spl_text

    @overrides
    def _add_specific_arguments(self, parser: argparse.ArgumentParser):
        super()._add_specific_arguments(parser)

        parser.add_argument('--embeddings-size', type=int, default=128,
                            help='The size used for generating sub-word embeddings')
        parser.add_argument('--hidden-dimension', type=int, default=256,
                            help='The dimension size used for hidden layers')
        parser.add_argument('--dropout', type=float, default=0.0,
                            help='Dropout probability')
        parser.add_argument('--number-of-layers', type=int, default=1,
                            help='Number of layers used for the RNN')
        parser.add_argument('--entity-tag-types', type=EntityTagType, choices=list(EntityTagType), default=[EntityTagType.Main], nargs='*',
                            help='Entity tag types that will be used for classification. Default is to only use `Main`')
        parser.add_argument("--no-attention", action='store_true',
                            help="whether to skip the attention layer")
        parser.add_argument("--bidirectional-rnn", action='store_true',
                            help="whether to use a bidirectional version of the RNN")
        parser.add_argument("--merge-subwords", action='store_true',
                            help="whether to merge the subword embeddings before passing through the RNN")
        parser.add_argument("--learn-character-embeddings", action='store_true',
                            help="whether to learn character embeddings next to the default subword ones")
        parser.add_argument('--character-embeddings-size', type=int, default=None,
                            help='The size used for generating character embeddings')
        parser.add_argument('--character-hidden-size', type=int, default=None,
                            help='The hidden size used for the character embeddings RNN')
        parser.add_argument("--replace-all-numbers", action='store_true',
                            help="If all numbers should be replaced by a hard-coded fixed string")
        parser.add_argument("--use-weighted-loss", action='store_true',
                            help="If set to true, CRF layer will use weighted loss which focuses more on non-empty tags")
        parser.add_argument("--use-manual-features", action='store_true',
                            help="If set to true, manual features representations will be learned and added to general embeddings")

    @property
    def entity_tag_types(self) -> List[EntityTagType]:
        return self._get_argument('entity_tag_types')

    @property
    def merge_subwords(self) -> bool:
        return self._get_argument('merge_subwords')

    @property
    def replace_all_numbers(self) -> int:
        return self._get_argument('replace_all_numbers')

    @property
    def use_attention(self) -> bool:
        return not self._get_argument('no_attention')

    @property
    def bidirectional_rnn(self) -> bool:
        return not self._get_argument('bidirectional_rnn')

    @property
    def learn_character_embeddings(self) -> bool:
        return self._get_argument('learn_character_embeddings')

    @property
    def character_embeddings_size(self) -> int:
        return self._get_argument('character_embeddings_size')

    @property
    def character_hidden_size(self) -> int:
        return self._get_argument('character_hidden_size')

    @property
    def use_weighted_loss(self) -> int:
        return self._get_argument('use_weighted_loss')

    @property
    def use_manual_features(self) -> bool:
        return self._get_argument('use_manual_features')

    @property
    def embeddings_size(self) -> int:
        return self._get_argument('embeddings_size')

    @property
    def hidden_dimension(self) -> int:
        return self._get_argument('hidden_dimension')

    @property
    def dropout(self) -> float:
        return self._get_argument('dropout')

    @property
    def number_of_layers(self) -> int:
        return self._get_argument('number_of_layers')
