from services.log_service import LogService
from services.arguments.arguments_service_base import ArgumentsServiceBase
from services.data_service import DataService
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from overrides import overrides
from models.model_base import ModelBase


class CharacterRNN(ModelBase):

    def __init__(
            self,
            data_service: DataService,
            arguments_service: ArgumentsServiceBase,
            log_service: LogService,
            vocabulary_size: int,
            character_embedding_size: int,
            hidden_size: int,
            number_of_layers: int,
            bidirectional_rnn: bool = True,
            dropout: float = 0.0):
        super().__init__(data_service, arguments_service, log_service)

        self._dropout = nn.Dropout(dropout)
        self._embedding_layer = nn.Embedding(vocabulary_size, character_embedding_size)
        self._character_rnn = nn.LSTM(
            character_embedding_size,
            hidden_size,
            num_layers=number_of_layers,
            batch_first=True,
            bidirectional=bidirectional_rnn)

    def forward(self, char_seq_tensor: torch.Tensor, char_seq_len: torch.Tensor) -> torch.Tensor:
        """
        Get the last hidden states of the LSTM
            input:
                char_seq_tensor: (batch_size, sent_len, word_length)
                char_seq_len: (batch_size, sent_len)
            output:
                Variable(batch_size, sent_len, char_hidden_dim )
        """
        batch_size = char_seq_tensor.size(0)
        sent_len = char_seq_tensor.size(1)
        char_seq_tensor = char_seq_tensor.view(batch_size * sent_len, -1)
        char_seq_len = char_seq_len.view(batch_size * sent_len)

        char_seq_len = torch.where(char_seq_len == 0, torch.ones(char_seq_len.shape, device=char_seq_len.device, dtype=char_seq_len.dtype), char_seq_len)

        sorted_seq_len, permIdx = char_seq_len.sort(0, descending=True)
        _, recover_idx = permIdx.sort(0, descending=False)
        sorted_seq_tensor = char_seq_tensor[permIdx]

        character_embeddings = self._embedding_layer.forward(sorted_seq_tensor)
        character_embeddings = self._dropout.forward(character_embeddings)
        pack_input = pack_padded_sequence(
            character_embeddings,
            sorted_seq_len.cpu(),
            batch_first=True)

        _, hidden = self._character_rnn.forward(pack_input, None)
        hidden = hidden[0].transpose(1, 0).contiguous().view(batch_size * sent_len, 1, -1)

        result = hidden[recover_idx].view(batch_size, sent_len, -1)
        return result
