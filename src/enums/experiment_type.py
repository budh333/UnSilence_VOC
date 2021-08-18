from enums.argument_enum import ArgumentEnum

class ExperimentType(ArgumentEnum):
    CosineSimilarity = 'cosine-similarity'
    CosineDistance = 'cosine-distance'
    EuclideanDistance = 'euclidean-distance'
    KLDivergence = 'kl-divergence'
    NeighbourhoodOverlap = 'neighbourhood-overlap'
    OverlapSetSizeComparison = 'overlap-set-size-comparison'