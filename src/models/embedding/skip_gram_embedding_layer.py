from copy import deepcopy
from services.log_service import LogService
from enums.language import Language

import torch.nn as nn
from torch.nn import init
from torch import nn


class SkipGramEmbeddingLayer(nn.Module):
    def __init__(
            self,
            log_service: LogService,
            language: Language,
            vocabulary_size: int,
            pretrained_matrix=None,
            randomly_initialized: bool = False,
            freeze_embeddings: bool = False,
            pad_token: int = 0):
        super().__init__()

        self._log_service = log_service

        if pretrained_matrix is not None:
            self._log_service.log_debug(
                'Pretrained matrix provided. Initializing embeddings from it')
            self._embeddings_target = nn.Embedding.from_pretrained(
                embeddings=deepcopy(pretrained_matrix),
                freeze=freeze_embeddings,
                sparse=True,
                padding_idx=pad_token)

            self._embeddings_context = nn.Embedding.from_pretrained(
                embeddings=deepcopy(pretrained_matrix),
                freeze=freeze_embeddings,
                sparse=True,
                padding_idx=pad_token)

            if randomly_initialized and not freeze_embeddings:
                embedding_size = pretrained_matrix.shape[-1]
                initrange = 1.0 / embedding_size
                init.uniform_(self._embeddings_target.weight.data, -initrange, initrange)
                init.constant_(self._embeddings_context.weight.data, 0)
        else:
            self._log_service.log_debug(
                'Pretrained matrix is not provided. Initializing embeddings randomly')
            embedding_size = self._get_embedding_size(language)
            self._embeddings_target = nn.Embedding(
                num_embeddings=vocabulary_size,
                embedding_dim=embedding_size,
                sparse=True,
                padding_idx=pad_token)

            self._embeddings_context = nn.Embedding(
                num_embeddings=vocabulary_size,
                embedding_dim=embedding_size,
                sparse=True,
                padding_idx=pad_token)

    def forward_target(self, target_words):
        target_embeddings = self._embeddings_target.forward(target_words)
        return target_embeddings

    def forward_context(self, context_words):
        context_embeddings = self._embeddings_context.forward(context_words)
        return context_embeddings

    def forward_negative(self, negative_examples):
        negative_embeddings = self._embeddings_context.forward(negative_examples)
        return negative_embeddings

    def _get_embedding_size(self, language: Language):
        if language == Language.English:
            return 300
        elif language == Language.Dutch:
            return 320
        elif language == Language.French:
            return 300
        elif language == Language.German:
            return 300

        raise NotImplementedError()
