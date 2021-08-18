import os
from services.log_service import LogService 
import torch
from overrides import overrides

from models.model_base import ModelBase
from transformers import PreTrainedModel, PretrainedConfig

from entities.models.model_checkpoint import ModelCheckpoint
from entities.metric import Metric

from services.arguments.pretrained_arguments_service import PretrainedArgumentsService
from services.data_service import DataService

class TransformerBase(ModelBase):
    def __init__(
            self,
            arguments_service: PretrainedArgumentsService,
            data_service: DataService,
            log_service: LogService,
            output_hidden_states: bool = False,
            overwrite_initialization: bool = False):
        super(TransformerBase, self).__init__(data_service, arguments_service, log_service)

        self._output_hidden_states = output_hidden_states

        if overwrite_initialization:
            self._log_service.log_debug('Skipping the initialization of the transformer model due to configuration settings')
            self._transformer_model = None
        else:
            self._log_service.log_debug(f'Initializing transformer model of type {str(self._model_type)} using \'{arguments_service.pretrained_weights}\' weights')

            config = self._config_type.from_pretrained(arguments_service.pretrained_weights, return_dict=True)
            config.output_hidden_states = output_hidden_states

            self._transformer_model: PreTrainedModel = self._model_type.from_pretrained(
                arguments_service.pretrained_weights,
                config=config)

        self._arguments_service = arguments_service

    @property
    def transformer_model(self) -> PreTrainedModel:
        return self._transformer_model

    @overrides
    def forward(self, input_batch, **kwargs):
        pass

    @overrides
    def named_parameters(self):
        return self._transformer_model.named_parameters()

    @overrides
    def parameters(self):
        return self._transformer_model.parameters()

    @overrides
    def compare_metric(self, best_metric: Metric, new_metrics: Metric) -> bool:
        if best_metric.is_new or best_metric.get_current_loss() > new_metrics.get_current_loss():
            return True

        return False

    @overrides
    def save(
            self,
            path: str,
            epoch: int,
            iteration: int,
            best_metrics: object,
            resets_left: int,
            name_prefix: str = None) -> bool:

        self._log_service.log_debug(f'Saving transformer model')

        model_name = self._get_model_name(name_prefix)

        saved = super().save(path, epoch, iteration, best_metrics,
                             resets_left, name_prefix, save_model_dict=False)

        if not saved:
            self._log_service.log_debug(f'Saving transformer model failed')
            return saved

        pretrained_weights_path = self._get_pretrained_path(
            path, model_name, create_if_missing=True)

        self._log_service.log_debug(f'Saving transformer model weights at \'{pretrained_weights_path}\'')
        self._transformer_model.save_pretrained(pretrained_weights_path)

        return saved

    @overrides
    def load(
            self,
            path: str,
            name_prefix: str = None,
            name_suffix: str = None,
            load_model_dict: bool = True,
            use_checkpoint_name: bool = True,
            checkpoint_name: str = None) -> ModelCheckpoint:

        model_name = self._get_model_name(name_prefix, name_suffix)

        model_checkpoint = super().load(
            path,
            model_name,
            load_model_dict=False,
            use_checkpoint_name=False)
        if model_checkpoint is None:
            return None

        if load_model_dict:
            self._load_transformer_model(path, model_name)

        return model_checkpoint

    @property
    def _model_type(self) -> type:
        return PreTrainedModel

    @property
    def _config_type(self) -> type:
        return PretrainedConfig

    def _load_transformer_model(self, path: str, name_prefix: str):
        pretrained_weights_path = self._get_pretrained_path(path, name_prefix)
        self._log_service.log_debug(f'Attempting to load transformer model weights from \'{pretrained_weights_path}\'')

        config = PretrainedConfig.from_pretrained(pretrained_weights_path)
        config.output_hidden_states = True

        self._transformer_model = self._model_type.from_pretrained(
            pretrained_weights_path, config=config).to(self._arguments_service.device)

    def _get_pretrained_path(self, path: str, name_prefix: str, create_if_missing: bool = False):
        file_name = f'{name_prefix}_weights'
        pretrained_weights_path = os.path.join(path, file_name)

        if create_if_missing and not os.path.exists(pretrained_weights_path):
            os.mkdir(pretrained_weights_path)

        return pretrained_weights_path