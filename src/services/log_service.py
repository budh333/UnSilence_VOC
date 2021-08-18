from datetime import datetime, timedelta
import os
from termcolor import colored
import wandb
import torch
import numpy as np
import json

from copy import deepcopy

from entities.metric import Metric
from entities.data_output_log import DataOutputLog
from services.arguments.arguments_service_base import ArgumentsServiceBase
import logging
from logging import Logger

from utils.dict_utils import stringify_dictionary

class LogService:
    def __init__(
            self,
            arguments_service: ArgumentsServiceBase,
            logger: Logger):

        self._arguments_service = arguments_service

        self._log_header = '  Time Epoch Iteration   Progress  (%Epoch) | Train Loss Train Accuracy | Validation Loss Val. Accuracy | Best'
        self._log_template = ' '.join(
            '{:>6.0f},{:>5.0f},{:>9.0f},{:>5.0f}/{:<5.0f} {:>7.0f}%,| {:>10.6f} {:>14.10f} | {:>15.11f} {:>13.9f} | {:>4s}'.split(','))

        self._start_time = datetime.now()

        self._progress_color = 'red'
        self._evaluation_color = 'cyan'

        self._current_epoch = 0
        self._all_iterations = 0
        self._current_iteration = 0

        config_name = self._arguments_service.get_configuration_name()
        self._run_name = f'{config_name}-{self._start_time.strftime("%Y_%m_%d_%H_%M_%S")}'

        self._logger: Logger = self._initialize_logger(logger)
        self.log_debug(f'Starting run \'{self._run_name}\'')

        self._external_logging_enabled = self._arguments_service.enable_external_logging
        if self._external_logging_enabled:
            wandb_project = str(self._arguments_service.challenge)
            wandb_entity = 'eval-historical-texts'
            wandb.init(
                project=wandb_project,
                config=self._arguments_service._arguments,
                entity=wandb_entity,
                force=True,
                name=config_name
                # resume=arguments_service.resume_training,
                # id='' #TODO
            )

            self.log_debug(
                f'W&B initialized [project: \'{wandb_project}\' entity: \'{wandb_entity}\' | name: \'{config_name}\'')

    def log_progress(
            self,
            current_step: int,
            all_steps: int,
            epoch_num: int = None,
            evaluation: bool = False):
        """Logs current progress of the training process

        :param current_step: Current step of the training process
        :type current_step: int
        :param all_steps: Amount of total steps in one epoch
        :type all_steps: int
        :param epoch_num: Current epoch number, defaults to None
        :type epoch_num: int, optional
        :param evaluation: Whether current progress is part of evaluation or training, defaults to False
        :type evaluation: bool, optional
        """

        prefix = 'Train'
        if evaluation:
            prefix = 'Evaluating'
        else:
            self.log_summary('Iteration', current_step)

        epoch_str = 'N/A'
        if epoch_num is not None:
            epoch_str = str(epoch_num)

        print(colored(
            f'{prefix}: {current_step}/{all_steps}       | Epoch: {epoch_str}           \r', self._progress_color), end='')

    def initialize_evaluation(self):
        self.log_debug('Starting training...')

        print(self._log_header)

    def log_evaluation(
            self,
            train_metric: Metric,
            validation_metric: Metric,
            epoch: int,
            iteration: int,
            iterations: int,
            new_best: bool,
            metric_log_key: str = None):
        """Logs current evaluation results

        :param train_metric: Metric of the training iterations
        :type train_metric: Metric
        :param validation_metric: Metric of the validation iterations
        :type validation_metric: Metric
        :param epoch: Current epoch number
        :type epoch: int
        :param iteration: Current iteration number
        :type iteration: int
        :param iterations: Total amount of iterations to perform
        :type iterations: int
        :param new_best: Whether the current result is a new best result
        :type new_best: bool
        :param metric_log_key: Whether a specific metric key should be used to display results. If None is provided, then accuracy is used, defaults to None
        :type metric_log_key: str, optional
        """
        self._current_epoch = epoch
        self._current_iteration = iteration
        self._all_iterations = iterations

        time_passed = self.get_time_passed()
        train_loss = train_metric.get_current_loss()
        train_accuracies = train_metric.get_current_accuracies()
        validation_loss = validation_metric.get_current_loss()
        validation_accuracies = validation_metric.get_current_accuracies()
        if train_accuracies and len(train_accuracies) > 0:
            if metric_log_key is not None and train_metric.contains_accuracy_metric(metric_log_key):
                train_accuracy = train_metric.get_accuracy_metric(
                    metric_log_key)
            else:
                train_accuracy = list(train_accuracies.values())[0]
        else:
            train_accuracy = 0

        if validation_accuracies and len(validation_accuracies) > 0:
            if metric_log_key is not None and validation_metric.contains_accuracy_metric(metric_log_key):
                validation_accuracy = validation_metric.get_accuracy_metric(
                    metric_log_key)
            else:
                validation_accuracy = list(validation_accuracies.values())[0]
        else:
            validation_accuracy = 0

        print(colored(
            self._log_template.format(
                time_passed.total_seconds(),
                epoch,
                iteration,
                1 + iteration,
                iterations,
                100. * (1 + iteration) / iterations,
                train_loss,
                train_accuracy,
                validation_loss,
                validation_accuracy,
                "BEST" if new_best else ""), self._evaluation_color))

        if self._external_logging_enabled:
            current_step = self._get_current_step()
            wandb.log({'Train loss': train_loss},
                      step=current_step)

            for key, value in train_accuracies.items():
                wandb.log({f'Train - {key}': value},
                          step=current_step)

            for key, value in validation_accuracies.items():
                wandb.log({f'Validation - {key}': value},
                          step=current_step)

            wandb.log({'Validation loss': validation_loss},
                      step=current_step)

            if current_step == 0:
                seconds_per_iteration = time_passed.total_seconds()
            else:
                seconds_per_iteration = time_passed.total_seconds() / current_step

            self.log_summary('Seconds per iteration', seconds_per_iteration)

    def log_info(self, message: str):
        self._logger.info(message)

    def log_debug(self, message: str):
        self._logger.debug(message)

    def log_error(self, message: str):
        self._logger.error(message)

    def log_exception(self, message: str, exception: Exception):
        log_message = f'Exception occurred. Message: {message}\nOriginal exception: {exception}'

        self._logger.exception(log_message)

    def log_warning(self, message: str):
        self._logger.warning(message)

    def log_summary(self, key: str, value: object):
        if not self._external_logging_enabled:
            return

        wandb.run.summary[key] = value

    def log_batch_results(self, data_output_log: DataOutputLog):
        """Logs batch results, using a data output log

        :param data_output_log: The data output log which contains the data to be logged
        :type data_output_log: DataOutputLog
        """
        if not self._external_logging_enabled or data_output_log is None:
            return

        columns, data = data_output_log.get_log_data()
        table_log = wandb.Table(columns=columns, data=data)

        wandb.log({
            'batch results': table_log
        }, step=self._get_current_step())

    def log_incremental_metric(self, metric_key: str, metric_value: object):
        if not self._external_logging_enabled:
            return

        wandb.log({
            metric_key: metric_value
        }, step=self._get_current_step())

    def log_heatmap(
            self,
            heatmap_title: str,
            matrix_values: np.array,
            x_labels: list,
            y_labels: list,
            show_text_inside: bool = False):
        if not self._external_logging_enabled:
            return

        wandb.log({
            heatmap_title: wandb.plots.HeatMap(
                x_labels,
                y_labels,
                matrix_values,
                show_text=show_text_inside)
        }, step=self._get_current_step())

    def start_logging_model(self, model: torch.nn.Module, criterion: torch.nn.Module = None):
        if not self._external_logging_enabled:
            return

        wandb.watch(model, criterion=criterion)

    def get_time_passed(self) -> timedelta:
        result = datetime.now() - self._start_time
        return result

    def _get_current_step(self) -> int:
        return (self._current_epoch * self._all_iterations) + self._current_iteration

    def _initialize_logger(self, logger: Logger) -> Logger:
        if len(logger.handlers) > 0:
            return logger

        log_folder = self._arguments_service.log_folder
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        log_file_name = f'{self._run_name}.log'
        log_file_path = os.path.join(
            self._arguments_service.log_folder, log_file_name)

        # create file handler which logs even debug messages
        file_handler = logging.FileHandler(log_file_path, encoding='utf8')
        file_handler.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        if self._arguments_service.verbose_logging:
            console_handler.setLevel(logging.DEBUG)
        else:
            console_handler.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)10s | %(message)s')
        file_handler.setFormatter(file_formatter)

        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)10s | %(message)s')
        console_handler.setFormatter(console_formatter)

        # add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def log_arguments(self):
        args = self._arguments_service.get_arguments_dict()
        args_string = stringify_dictionary(args)
        self.log_debug(f'arguments initialized: {args_string}')

    def __deepcopy__(self, memo):
        # we do not want log service to be re-initialized, so we just return the current object
        return self