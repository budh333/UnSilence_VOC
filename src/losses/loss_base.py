import torch.nn as nn

class LossBase(nn.Module):
    def __init__(self):
        super(LossBase, self).__init__()

    def backward(self, model_output):
        return 0.0

    def calculate_loss(self, model_output):
        return 0.0

    @property
    def criterion(self) -> nn.Module:
        return None