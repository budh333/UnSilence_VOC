import os

from enums.language import Language

from services.arguments.arguments_service_base import ArgumentsServiceBase


class FileService:
    def __init__(
            self,
            arguments_service: ArgumentsServiceBase):

        self._arguments_service = arguments_service

    def get_initial_data_path(self) -> str:
        data_path = self._arguments_service.data_folder
        return data_path

    def get_data_path(
        self,
        language: Language = None) -> str:
        """Get the data path that is provided using input arguments

        :param language: Language to be used. If None is provided, the one provided from the arguments will be used, defaults to None
        :type language: Language, optional
        :return: The path to the data
        :rtype: str
        """

        data_path = self.get_challenge_path()

        data_model_path = os.path.join(
            data_path,
            str(self._arguments_service.configuration))

        if not os.path.exists(data_model_path):
            os.mkdir(data_model_path)

        if language is None:
            language = self._arguments_service.language

        data_language_path = os.path.join(
            data_model_path,
            str(language))

        if not os.path.exists(data_language_path):
            os.mkdir(data_language_path)

        return data_language_path

    def get_checkpoints_path(self) -> str:
        """Get the path to the checkpoints

        :return: Path to the checkpoints
        :rtype: str
        """
        if not self._arguments_service.checkpoint_folder:
            output_path = self._arguments_service.output_folder
        else:
            output_path = self._arguments_service.checkpoint_folder

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        challenge_name = str(self._arguments_service.challenge)
        if challenge_name:
            output_path = os.path.join(output_path, challenge_name)
            if not os.path.exists(output_path):
                os.mkdir(output_path)

        output_model_path = os.path.join(
            output_path,
            str(self._arguments_service.configuration))

        if not os.path.exists(output_model_path):
            os.mkdir(output_model_path)

        model_path = os.path.join(
            output_model_path,
            str(self._arguments_service.language))

        if not os.path.exists(model_path):
            os.mkdir(model_path)

        return model_path

    def get_challenge_path(self) -> str:
        """Get the path for the initialized challenge. This would a path inside the data folder

        :return: The challenge path
        :rtype: str
        """
        data_path = self._arguments_service.data_folder

        if not os.path.exists(data_path):
            os.mkdir(data_path)

        challenge_name = str(self._arguments_service.challenge)
        if challenge_name:
            data_path = os.path.join(data_path, challenge_name)
            if not os.path.exists(data_path):
                os.mkdir(data_path)

        return data_path

    def get_pickles_path(self) -> str:
        """Get the generic path to where the pickles are stored for this challenge

        :return: The pickles path
        :rtype: str
        """
        data_path = self.get_challenge_path()

        data_pickles_path = os.path.join(data_path, 'pickles')

        if not os.path.exists(data_pickles_path):
            os.mkdir(data_pickles_path)

        return data_pickles_path

    def get_experiments_path(self) -> str:
        """Get the path where experiments are being saved

        :return: The experiments path
        :rtype: str
        """
        experiments_path = self._arguments_service.experiments_folder

        if not os.path.exists(experiments_path):
            os.mkdir(experiments_path)

        return experiments_path

    def combine_path(self, path: str, *paths: str, create_if_missing: bool = False) -> str:
        """Combine multiple paths and optionally create all folders along the path if they are missing

        :param path: The original path
        :type path: str
        :param create_if_missing: Create all folders along the path if they are missing, defaults to False
        :type create_if_missing: bool, optional
        :raises Exception: If the path does not exist and the create_if_missing is False
        :return: The concatenated path
        :rtype: str
        """
        if create_if_missing and not os.path.exists(path):
            os.mkdir(path)

        if paths is None or len(paths) == 0:
            return path

        final_path = path
        for path_extension in paths:
            final_path = os.path.join(final_path, path_extension)
            if not os.path.exists(final_path):
                if create_if_missing:
                    os.mkdir(final_path)
                else:
                    raise Exception(f'Path "{final_path}" does not exist')

        return final_path