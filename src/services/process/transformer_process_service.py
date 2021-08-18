# from entities.cache.cache_options import CacheOptions
# from typing import List, Tuple
# import random

# from enums.ocr_output_type import OCROutputType

# from entities.transformers.transformer_entry import TransformerEntry

# from services.process.process_service_base import ProcessServiceBase
# from services.tokenize.base_tokenize_service import BaseTokenizeService

# from services.vocabulary_service import VocabularyService
# from services.cache_service import CacheService
# from services.log_service import LogService


# class TransformerProcessService(ProcessServiceBase):
#     def __init__(
#             self,
#             arguments_service: OCRQualityArgumentsService,
#             tokenize_service: BaseTokenizeService,
#             cache_service: CacheService,
#             log_service: LogService):
#         super().__init__()

#         self._arguments_service = arguments_service
#         self._tokenize_service = tokenize_service
#         self._cache_service = cache_service
#         self._log_service = log_service

#         self._preprocess_max_string_length = 128

#     def get_entries(self, ocr_output_type: OCROutputType):
#         entries = None
#         limit_size = self._arguments_service.train_dataset_limit_size

#         entries = self._load_transformer_entries(
#             ocr_output_type,
#             limit_size)

#         return entries

#     def _generate_entries(self):
#         self._ocr_download_service.download_data(
#             self._arguments_service.language, max_string_length=self._preprocess_max_string_length)

#         ocr_file_data, gs_file_data = self._read_data()

#         encoded_ocr_sequences = self._tokenize_service.encode_sequences(
#             ocr_file_data)
#         encoded_gs_sequences = self._tokenize_service.encode_sequences(
#             gs_file_data)

#         ocr_entries = [TransformerEntry(i, ids, special_tokens_mask)
#                        for i, (ids, _, _, special_tokens_mask) in enumerate(encoded_ocr_sequences)]
#         gs_entries = [TransformerEntry(i, ids, special_tokens_mask)
#                       for i, (ids, _, _, special_tokens_mask) in enumerate(encoded_gs_sequences)]

#         return ocr_entries, gs_entries

#     def _load_transformer_entries(
#             self,
#             ocr_output_type: OCROutputType,
#             reduction: int) -> List[TransformerEntry]:
#         ocr_entries, gs_entries = self._cache_service.get_item_from_cache(
#             CacheOptions(f'entries-{self._get_datasets_string()}'),
#             callback_function=self._generate_entries)

#         entries = ocr_entries if ocr_output_type == OCROutputType.Raw else gs_entries

#         total_amount = len(entries)
#         if reduction is not None:
#             entries = entries[:reduction]

#         self._log_service.log_info(
#             f'Loaded {len(entries)} entries out of {total_amount} total')
#         self._log_service.log_summary(
#             key=f'entries amount', value=len(entries))

#         return entries

#     def _load_file_data(self):
#         number_of_files = len(self._arguments_service.datasets)

#         ocr_file_data = []
#         gs_file_data = []

#         for i, dataset in enumerate(self._arguments_service.datasets):
#             print(f'{i}/{number_of_files}             \r', end='')
#             result = self._ocr_download_service.get_downloaded_dataset(
#                 dataset, self._preprocess_max_string_length)
#             if result is None:
#                 self._log_service.log_warning(
#                     f'Did not find \'{dataset}\' dataset to load')
#                 continue
#             else:
#                 self._log_service.log_debug(f'Loading \'{dataset}\' data')

#             ocr_file_data.extend(result[0])
#             gs_file_data.extend(result[1])

#         return ocr_file_data, gs_file_data

#     def _read_data(self):

#         (ocr_file_data, gs_file_data) = self._cache_service.get_item_from_cache(
#             CacheOptions(
#                 f'ocr-gs-file-data-{self._get_datasets_string()}-{self._preprocess_max_string_length}',
#                 configuration_specific=False),
#             callback_function=self._load_file_data)

#         return ocr_file_data, gs_file_data
