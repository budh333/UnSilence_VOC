import torch
import torch.nn as nn

from overrides import overrides

from losses.loss_base import LossBase

class NERLoss(LossBase):
    def __init__(self):
        super().__init__()

    @overrides
    def backward(self, model_output):
        loss = self._calculate_inner_loss(model_output)
        loss.backward()

        return loss.item()

    @overrides
    def calculate_loss(self, model_output):
        loss = self._calculate_inner_loss(model_output)
        return loss.item()

    def _calculate_inner_loss(self, model_output):
        _, losses, _ = model_output
        return torch.stack(list(losses.values())).sum()