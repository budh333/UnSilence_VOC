from overrides import overrides

import torch
import torch.nn as nn

from losses.loss_base import LossBase

class CrossEntropyLoss(LossBase):
    def __init__(self):
        super().__init__()

        self._criterion = nn.CrossEntropyLoss()

    @overrides
    def backward(self, model_output):
        prediction, target = model_output
        loss = self._criterion.forward(prediction, target)
        loss.backward()

        return loss.item()

    @overrides
    def calculate_loss(self, model_output) -> torch.Tensor:
        prediction, target = model_output
        loss = self._criterion.forward(prediction, target)
        return loss.item()


    @property
    @overrides
    def criterion(self) -> nn.Module:
        return self._criterion