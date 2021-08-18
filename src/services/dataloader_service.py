from services.log_service import LogService
import numpy as np

from typing import Tuple

import torch
from torch.utils.data import DataLoader

from transformers import BertTokenizer

from enums.run_type import RunType

from services.arguments.arguments_service_base import ArgumentsServiceBase
from services.dataset_service import DatasetService
from services.tokenize.base_tokenize_service import BaseTokenizeService


class DataLoaderService:

    def __init__(
            self,
            arguments_service: ArgumentsServiceBase,
            dataset_service: DatasetService,
            log_service: LogService):

        self._dataset_service = dataset_service
        self._arguments_service = arguments_service
        self._log_service = log_service

    def get_train_dataloaders(self) -> Tuple[DataLoader, DataLoader]:
        """Loads and returns train and validation(if available) dataloaders

        :return: the dataloaders
        :rtype: Tuple[DataLoader, DataLoader]
        """
        data_loader_train = self._initialize_dataloader(
            run_type=RunType.Train,
            batch_size=self._arguments_service.batch_size,
            shuffle=self._arguments_service.shuffle)

        data_loader_validation = None
        if not self._arguments_service.skip_validation:
            data_loader_validation = self._initialize_dataloader(
                run_type=RunType.Validation,
                batch_size=self._arguments_service.batch_size,
                shuffle=False)

        return (data_loader_train, data_loader_validation)

    def get_test_dataloader(self) -> DataLoader:
        """Loads and returns the test dataloader

        :return: the test dataloader
        :rtype: DataLoader
        """
        data_loader_test = self._initialize_dataloader(
            run_type=RunType.Test,
            batch_size=self._arguments_service.batch_size,
            shuffle=False)

        return data_loader_test

    def _initialize_dataloader(
            self,
            run_type: RunType,
            batch_size: int,
            shuffle: bool) -> DataLoader:

        self._log_service.log_debug(
            f'Initializing dataset for run type \'{run_type.value}\'')
        dataset = self._dataset_service.initialize_dataset(run_type)
        data_loader: DataLoader = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=shuffle)

        if dataset.use_collate_function():
            data_loader.collate_fn = dataset.collate_function

        self._log_service.log_debug(
            f'Created dataloader for run type \'{run_type.value}\' [shuffle: {shuffle} | batch size: {batch_size} | collate function: {dataset.use_collate_function()}]')
        return data_loader
