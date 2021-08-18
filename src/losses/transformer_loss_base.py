from overrides import overrides

from losses.loss_base import LossBase

class TransformerLossBase(LossBase):
    def __init__(self):
        super().__init__()

    @overrides
    def backward(self, model_output):
        # print(model_output)
        # model_output.mean().backward()
        model_output.backward()

        return model_output.item()

    @overrides
    def calculate_loss(self, model_output):
        loss = model_output
        return loss.item()
