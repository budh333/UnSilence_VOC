from torch.utils.data import Dataset

from overrides import overrides

class DatasetBase(Dataset):
    def __init__(self, **kwargs):
        super().__init__()

    def __len__(self) -> int:
        return len(super())

    @overrides
    def __getitem__(self, idx):
        return super().__getitem__(idx)

    def use_collate_function(self) -> bool:
        return False

    def collate_function(self, sequences):
        pass
