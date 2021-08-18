from enums.challenge import Challenge
from enums.configuration import Configuration
from enums.run_type import RunType

from datasets.dataset_base import DatasetBase
from datasets.ner_dataset import NERDataset

from services.arguments.arguments_service_base import ArgumentsServiceBase
from services.file_service import FileService
from services.mask_service import MaskService
from services.tokenize.base_tokenize_service import BaseTokenizeService
from services.log_service import LogService
from services.vocabulary_service import VocabularyService
from services.metrics_service import MetricsService
from services.data_service import DataService
from services.process.process_service_base import ProcessServiceBase


class DatasetService:
    def __init__(
            self,
            arguments_service: ArgumentsServiceBase,
            mask_service: MaskService,
            process_service: ProcessServiceBase,
            vocabulary_service: VocabularyService,
            log_service: LogService):

        self._arguments_service = arguments_service
        self._mask_service = mask_service
        self._process_service = process_service
        self._vocabulary_service = vocabulary_service
        self._log_service = log_service

    def initialize_dataset(self, run_type: RunType) -> DatasetBase:
        """Loads and returns the dataset based on run type ``(Train, Validation, Test)`` and the language

        :param run_type: used to distinguish which dataset should be returned
        :type run_type: RunType
        :rtype: DatasetBase
        """
        joint_model: bool = self._arguments_service.joint_model
        configuration: Configuration = self._arguments_service.configuration
        challenge: Challenge = self._arguments_service.challenge
        result = None

        if run_type == RunType.Test:
            pass

        if not joint_model:
            if challenge == Challenge.OCREvaluation:
                self._log_service.log_debug('Initializing NER dataset')
                result = NERDataset(
                    arguments_service=self._arguments_service,
                    vocabulary_service=self._vocabulary_service,
                    process_service=self._process_service,
                    log_service=self._log_service)

        return result
