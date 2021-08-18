from overrides import overrides

import torch
import torch.nn.functional as F

from losses.loss_base import LossBase

class SkipGramLoss(LossBase):
    def __init__(self):
        super().__init__()

    @overrides
    def backward(self, embeddings):
        loss = self._calculate_loss(embeddings)
        loss.backward()
        return loss.item()

    @overrides
    def calculate_loss(self, embeddings) -> torch.Tensor:
        loss = self._calculate_loss(embeddings)
        return loss.item()

    def _calculate_loss(self, embeddings):
        (emb_target, emb_context, emb_negative) = embeddings
        emb_target = emb_target.unsqueeze(2)

        pos_loss = torch.bmm(emb_context, emb_target)
        pos_loss = -F.logsigmoid(pos_loss)

        neg_loss = torch.bmm(emb_negative, emb_target).squeeze()
        neg_loss = -torch.sum(F.logsigmoid(-neg_loss), dim=1)
        total_loss = torch.mean(pos_loss + neg_loss)
        return total_loss