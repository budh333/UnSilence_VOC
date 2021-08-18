from typing import List

from MulticoreTSNE import MulticoreTSNE as TSNE
import numpy as np


class FitTransformationService:
    def __init__(self):
        pass

    def fit_and_transform_vectors(
        self,
        number_of_components: int,
        vectors: list):
        """Fits a list of vectors using TSNE into `number_of_components`

        :param number_of_components: The number of components the vectors will be fitted into
        :type number_of_components: int
        :param vectors: The vectors to be fitted in
        :type vectors: list
        :return: Returns the TSNE result
        :rtype: [type]
        """

        tsne = TSNE(
            n_components=number_of_components,
            random_state=0,
            n_jobs=4)

        if not isinstance(vectors, np.ndarray):
            vectors = np.array(vectors)

        tsne_result = tsne.fit_transform(vectors)
        return tsne_result