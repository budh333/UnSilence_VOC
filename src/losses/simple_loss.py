from overrides import overrides

import torch
import torch.nn as nn

from losses.loss_base import LossBase

class SimpleLoss(LossBase):
    def __init__(self):
        super().__init__()

    @overrides
    def backward(self, loss):
        loss.backward()
        return loss.item()

    @overrides
    def calculate_loss(self, loss) -> torch.Tensor:
        return loss.item()