import csv
import os

from typing import List, Dict
from overrides import overrides

import torch

from entities.batch_representation import BatchRepresentation

from enums.evaluation_type import EvaluationType
from enums.entity_tag_type import EntityTagType
from enums.language import Language

from services.arguments.ner_arguments_service import NERArgumentsService
from services.file_service import FileService
from services.evaluation.base_evaluation_service import BaseEvaluationService
from services.plot_service import PlotService
from services.metrics_service import MetricsService
from services.process.ner_process_service import NERProcessService
from services.string_process_service import StringProcessService


class NEREvaluationService(BaseEvaluationService):
    def __init__(
            self,
            arguments_service: NERArgumentsService,
            file_service: FileService,
            process_service: NERProcessService,
            string_process_service: StringProcessService):
        super().__init__()

        self._arguments_service = arguments_service
        self._process_service = process_service
        self._file_service = file_service
        self._string_process_service = string_process_service

    @overrides
    def evaluate_batch(
            self,
            output: torch.Tensor,
            batch_input: BatchRepresentation,
            evaluation_types: List[EvaluationType],
            batch_index: int) -> Dict[EvaluationType, List]:
        predictions = output[0]

        result = []
        for entity_tag_type, type_predictions in predictions.items():
            for i, prediction in enumerate(type_predictions.squeeze(0).cpu().detach().tolist()):
                predicted_entity = self._process_service.get_entity_by_label(prediction, entity_tag_type, ignore_unknown=True)
                if len(result) <= i:
                    result.append({})

                result[i][entity_tag_type] = predicted_entity

        evaluation = {EvaluationType.NamedEntityRecognitionMatch: result}
        return evaluation

    def save_results(self, evaluation: Dict[EvaluationType, List]):
        challenge_path = self._file_service.get_challenge_path()
        language_suffix = self._get_language_suffix(self._arguments_service.language)
        test_filepath = os.path.join(challenge_path, f'data-test-{language_suffix}.tsv')

        predictions = evaluation[EvaluationType.NamedEntityRecognitionMatch]

        tokens: List[str] = []
        with open(test_filepath, 'r', encoding='utf-8') as test_tsv:
            reader = csv.DictReader(test_tsv, dialect=csv.excel_tab, quoting=csv.QUOTE_NONE)
            header = reader.fieldnames
            for row in reader:
                tokens.append(row['TOKEN'])

        test_word_amount = len([x for x in tokens if x is not None and not x.startswith('#')])
        # assert len(predictions) == test_word_amount, f'Got "{len(predictions)}" predictions but expected "{test_word_amount}"'

        column_mapping = {
            EntityTagType.Main: 'NE-MAIN',
            EntityTagType.Name: 'NE-PER-NAME',
            EntityTagType.Gender: 'NE-PER-GENDER',
            EntityTagType.LegalStatus: 'NE-PER-LEGAL-STATUS',
            EntityTagType.Role: 'NE-PER-ROLE',
            EntityTagType.OrganizationBeneficiary: 'NE-ORG-BENEFICIARY'
        }

        checkpoints_path = self._file_service.get_checkpoints_path()
        file_path = os.path.join(
            checkpoints_path, f'output-{self._arguments_service.get_configuration_name()}.tsv')
        with open(file_path, 'w', encoding='utf-8') as output_tsv:
            writer = csv.DictWriter(output_tsv, dialect=csv.excel_tab, fieldnames=header)
            writer.writeheader()

            counter = 0
            for token in tokens:
                skip_prediction = self._string_process_service._clean_up_word(token) == ''
                if skip_prediction:
                    row_dict = { column_name: 'O' for column_name in column_mapping.values() }
                    row_dict['TOKEN'] = token   
                    writer.writerow(row_dict)
                elif token.startswith('#'):
                    writer.writerow({'TOKEN': token})
                else:
                    row_dict = { column_mapping[entity_tag_type]: prediction for entity_tag_type, prediction in predictions[counter].items() }
                    row_dict['TOKEN'] = token
                    writer.writerow(row_dict)

                    counter += 1

        return file_path

    def _get_language_suffix(self, language: Language)  -> str:
        if language == Language.Dutch:
            return 'nl'
        else:
            raise Exception(f'Unsupported language for evaluation - {language}')