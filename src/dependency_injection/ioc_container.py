from losses.ner_loss import NERLoss
from services.tag_metrics_service import TagMetricsService
from models.transformers.bert_model import BertModel
from services.process.ner_process_service import NERProcessService
from optimizers.sparse_adam_optimizer import SparseAdamOptimizer
from services.fit_transformation_service import FitTransformationService
from services.tagging_service import TaggingService

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dependency_injection.selector_utils import *

import main

from losses.loss_base import LossBase

from models.model_base import ModelBase
from models.ner_rnn.ner_predictor import NERPredictor

from optimizers.optimizer_base import OptimizerBase
from optimizers.sgd_optimizer import SGDOptimizer
from optimizers.adam_optimizer import AdamOptimizer
from optimizers.adamw_transformer_optimizer import AdamWTransformerOptimizer

from services.arguments.ner_arguments_service import NERArgumentsService
from services.arguments.arguments_service_base import ArgumentsServiceBase

from services.process.process_service_base import ProcessServiceBase

from services.data_service import DataService
from services.dataloader_service import DataLoaderService
from services.dataset_service import DatasetService
from services.file_service import FileService
from services.log_service import LogService
from services.mask_service import MaskService
from services.metrics_service import MetricsService
from services.test_service import TestService

from services.tokenize.base_tokenize_service import BaseTokenizeService
from services.tokenize.bert_tokenize_service import BERTTokenizeService

from services.train_service import TrainService
from services.vocabulary_service import VocabularyService
from services.plot_service import PlotService
from services.cache_service import CacheService
from services.string_process_service import StringProcessService

import logging


class IocContainer(containers.DeclarativeContainer):
    """Application IoC container."""

    logger = providers.Singleton(
        logging.Logger,
        name='historical-ocr logger')

    # Services

    arguments_service_base = providers.Singleton(
        ArgumentsServiceBase,
        raise_errors_on_invalid_args=False)

    argument_service_selector = providers.Callable(
        get_arguments_service,
        arguments_service=arguments_service_base)

    arguments_service: providers.Provider[ArgumentsServiceBase] = providers.Selector(
        argument_service_selector,
        base=providers.Singleton(ArgumentsServiceBase),
        ner=providers.Singleton(
            NERArgumentsService))

    log_service = providers.Singleton(
        LogService,
        arguments_service=arguments_service,
        logger=logger)

    data_service = providers.Factory(
        DataService,
        log_service=log_service)

    file_service = providers.Factory(
        FileService,
        arguments_service=arguments_service
    )

    cache_service = providers.Singleton(
        CacheService,
        arguments_service=arguments_service,
        file_service=file_service,
        data_service=data_service,
        log_service=log_service)

    plot_service = providers.Factory(
        PlotService,
        data_service=data_service
    )

    vocabulary_service: providers.Provider[VocabularyService] = providers.Singleton(
        VocabularyService,
        data_service=data_service,
        file_service=file_service,
        cache_service=cache_service,
        log_service=log_service
    )

    string_process_service = providers.Factory(StringProcessService)

    tokenize_service_selector = providers.Callable(
        get_tokenize_service,
        arguments_service=arguments_service)

    tokenize_service: providers.Provider[BaseTokenizeService] = providers.Selector(
        tokenize_service_selector,
        bert=providers.Singleton(
            BERTTokenizeService,
            arguments_service=arguments_service,
            file_service=file_service))

    mask_service = providers.Factory(
        MaskService,
        tokenize_service=tokenize_service,
        arguments_service=arguments_service
    )

    metrics_service = providers.Factory(MetricsService)

    tagging_service = providers.Factory(TaggingService)

    process_service_selector = providers.Callable(
        get_process_service,
        arguments_service=arguments_service)

    process_service: providers.Provider[ProcessServiceBase] = providers.Selector(
        process_service_selector,
        ner=providers.Singleton(
            NERProcessService,
            arguments_service=arguments_service,
            vocabulary_service=vocabulary_service,
            file_service=file_service,
            tokenize_service=tokenize_service,
            data_service=data_service,
            cache_service=cache_service,
            string_process_service=string_process_service))

    dataset_service = providers.Factory(
        DatasetService,
        arguments_service=arguments_service,
        mask_service=mask_service,
        process_service=process_service,
        vocabulary_service=vocabulary_service,
        log_service=log_service)

    dataloader_service = providers.Factory(
        DataLoaderService,
        arguments_service=arguments_service,
        dataset_service=dataset_service,
        log_service=log_service)

    tag_metrics_service = providers.Factory(
        TagMetricsService
    )

    model_selector = providers.Callable(
        get_model_type,
        arguments_service=arguments_service)

    model: providers.Provider[ModelBase] = providers.Selector(
        model_selector,
        bi_lstm_crf=providers.Singleton(
            NERPredictor,
            arguments_service=arguments_service,
            data_service=data_service,
            metrics_service=metrics_service,
            process_service=process_service,
            tokenize_service=tokenize_service,
            file_service=file_service,
            tag_metrics_service=tag_metrics_service,
            log_service=log_service))
    # bert=providers.Singleton(
    #     BERT,
    #     arguments_service=arguments_service,
    #     data_service=data_service,
    #     log_service=log_service,
    #     tokenize_service=tokenize_service))

    loss_selector = providers.Callable(
        get_loss_function,
        arguments_service=arguments_service)

    loss_function: providers.Provider[LossBase] = providers.Selector(
        loss_selector,
        base=providers.Singleton(LossBase),
        ner=providers.Singleton(NERLoss))

    optimizer_selector = providers.Callable(
        get_optimizer,
        arguments_service=arguments_service)

    optimizer: providers.Provider[OptimizerBase] = providers.Selector(
        optimizer_selector,
        base=providers.Singleton(
            OptimizerBase,
            arguments_service=arguments_service,
            model=model),
        sgd=providers.Singleton(
            SGDOptimizer,
            arguments_service=arguments_service,
            model=model),
        adam=providers.Singleton(
            AdamOptimizer,
            arguments_service=arguments_service,
            model=model),
        sparse_adam=providers.Singleton(
            SparseAdamOptimizer,
            arguments_service=arguments_service,
            model=model),
        transformer=providers.Singleton(
            AdamWTransformerOptimizer,
            arguments_service=arguments_service,
            model=model))

    fit_transformation_service = providers.Factory(
        FitTransformationService)

    test_service = providers.Factory(
        TestService,
        arguments_service=arguments_service,
        dataloader_service=dataloader_service,
        file_service=file_service,
        model=model
    )

    train_service_selector = providers.Callable(
        include_train_service,
        arguments_service=arguments_service)

    train_service: providers.Provider[TrainService] = providers.Selector(
        train_service_selector,
        include=providers.Factory(
            TrainService,
            arguments_service=arguments_service,
            dataloader_service=dataloader_service,
            loss_function=loss_function,
            optimizer=optimizer,
            log_service=log_service,
            model=model,
            file_service=file_service),
        exclude=providers.Object(None))

    # Misc

    main = providers.Callable(
        main.main,
        arguments_service=arguments_service,
        train_service=train_service,
        test_service=test_service,
        log_service=log_service)
