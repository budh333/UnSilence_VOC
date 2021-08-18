from enum import Enum

class WordEvaluationType(Enum):
    CurrentRaw = 0
    CurrentGT = 1
    Baseline = 2
    CurrentOriginal = 3