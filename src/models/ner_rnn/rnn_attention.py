import math
from services.log_service import LogService
from services.arguments.arguments_service_base import ArgumentsServiceBase
from services.data_service import DataService
import torch
from torch import nn
from torch.functional import F

from overrides import overrides
from models.model_base import ModelBase

class RNNAttention(ModelBase):
  def __init__(
    self,
    data_service: DataService,
    arguments_service: ArgumentsServiceBase,
    log_service: LogService,
    query_dim):
    super().__init__(data_service, arguments_service, log_service)
    self.scale = 1. / math.sqrt(query_dim)

 
  def forward(self, query, keys, values):
    # Query = [BxQ]
    # Keys = [TxBxK]
    # Values = [TxBxV]
    # Outputs = a:[TxB], lin_comb:[BxV]

    # Here we assume q_dim == k_dim (dot product attention)

    query = query.unsqueeze(1) # [BxQ] -> [Bx1xQ]
    keys = keys.transpose(1,2) # [TxBxK] -> [BxKxT]
    energy = torch.bmm(query, keys) # [Bx1xQ]x[BxKxT] -> [Bx1xT]
    energy = F.softmax(energy.mul_(self.scale), dim=2) # scale, normalize

    linear_combination = torch.bmm(energy, values) #[Bx1xT]x[BxTxV] -> [BxV]
    return energy, linear_combination