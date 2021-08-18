from matplotlib.figure import Figure
from services.log_service import LogService
import _pickle as pickle
import os
from collections import defaultdict
from datetime import datetime
import time
import logging
from typing import List, Callable

import matplotlib.pyplot as plt

class DataService:

    def __init__(
        self,
        log_service: LogService):

        self._log_service = log_service

        # determines relative disk directory for saving/loading
        self.stamp: str = ''
        self.actual_date: datetime = None

    def save_python_obj(self, obj: object, path: str, name: str) -> bool:
        """Saves python object to the file system as a pickle

        :param obj: the object to be saved
        :type obj: object
        :param path: path to the folder where the file will be saved
        :type path: str
        :param name: name of the file to be created
        :type name: str
        :param print_success: if true, successfull result will be printed to the console, defaults to True
        :type print_success: bool, optional
        :return: whether the save was successfull
        :rtype: bool
        """
        self._log_service.log_debug(f'Saving python object [path: \'{path}\' | name: \'{name}\']')

        try:
            filepath = os.path.join(path, f'{name}.pickle')
            with open(filepath, 'wb') as handle:
                pickle.dump(obj, handle, protocol=-1)

                self._log_service.log_debug(f'Saved successfully {name}')

            return True
        except Exception as e:
            self._log_service.log_exception(f'Failed saving {name}, continue anyway', e)
            return False

    def check_python_object(
        self,
        path: str,
        name: str,
        extension_included: bool = False) -> bool:
        extension = '' if extension_included else '.pickle'
        filepath = os.path.join(path, f'{name}{extension}')
        result = (os.path.exists(filepath) and os.stat(filepath).st_size > 0)
        self._log_service.log_debug(f'Checking python object {name}. Result - {result} [path: \'{filepath}\']')

        return result

    def load_python_obj(
        self,
        path: str,
        name: str,
        extension_included: bool = False) -> object:
        """Loads python object from disk if is pickled already

        :param path: path to the folder where the object pickle is located
        :type path: str
        :param name: name of the pickle file
        :type name: str
        :return: the unpickled object
        :rtype: object
        """
        self._log_service.log_debug(f'Loading python object [path: \'{path}\' | name: \'{name}\']')
        obj = None
        try:
            extension = '' if extension_included else '.pickle'
            filepath = os.path.join(path, f'{name}{extension}')
            with (open(filepath, "rb")) as openfile:
                obj = pickle.load(openfile)

        except FileNotFoundError:
            self._log_service.log_warning(f'{name} not loaded because file is missing')

            return None

        self._log_service.log_debug(f'Loaded python object {name}. [path: \'{filepath}\']')
        return obj

    def python_obj_exists(self, path: str, name: str) -> bool:
        """Checks if python object exists as a pickle on the file system

        :param path: path where the object pickle should be located
        :type path: str
        :param name: name of the pickle file
        :type name: str
        :return: result showing if the file exists or not
        :rtype: bool
        """
        filepath = os.path.join(path, f'{name}.pickle')
        result = os.path.exists(filepath)
        return result

    def personal_deepcopy(self, obj: object) -> object:
        """Deep copies any object faster than builtin

        :param obj: object to be deep-copied
        :type obj: object
        :return: the new deep-copied object
        :rtype: object
        """

        return pickle.loads(pickle.dumps(obj, protocol=-1))

    def duplicate_list(self, lst: list) -> list:
        """shallow copies list

        :param lst: list to be copied
        :type lst: list
        :return: the new list copy
        :rtype: list
        """

        return [x for x in lst]

    def duplicate_set(self, st: set) -> set:
        """shallow copies set

        :param st: the set to be copied
        :type st: set
        :return: the new set copy
        :rtype: set
        """

        return {x for x in st}

    def duplicate_dict(self, dc: dict) -> dict:
        """shallow copies dictionary

        :param dc: the dictionary to be copied
        :type dc: dict
        :return: the new dict copy
        :rtype: dict
        """

        return {key: dc[key] for key in dc}

    def duplicate_default_dict(
            self,
            dfdc: defaultdict,
            type_func: Callable,
            dictionary_type: type) -> defaultdict:
        """shallow copies a default dictionary but gives the chance to also shallow copy its members

        :param dfdc: the default dictionary that will be duplicated
        :type dfdc: defaultdict
        :param type_func: the function that will be used for duplicating
        :type type_func: function
        :param dictionary_type: the type of the default dictionary
        :type dictionary_type: [type]
        :return: the new default dictionary copy
        :rtype: defaultdict
        """

        output = defaultdict(dictionary_type)
        for key in dfdc:
            output[key] = type_func(dfdc[key])

        return output

    def dump_only(self, obj: object) -> bytes:
        """Dumps a python object into a pickle without saving to the file system

        :param obj: object to be pickled
        :type obj: object
        :return: the pickled object
        :rtype: bytes
        """
        return pickle.dumps(obj, protocol=-1)

    def load_only(self, obj: bytes) -> object:
        """Loads a pickled object

        :param obj: the encoded pickle object
        :type obj: bytes
        :return: the decoded python object
        :rtype: object
        """
        return pickle.loads(obj)

    def save_figure(self, path: str, name: str, extension: str = 'png', fig: Figure = None):
        """saves figure to the file system

        :param path: path to the folder where the figure should be saved
        :type path: str
        :param name: name of the file to be created
        :type name: str
        :param extension: extension of the figure file, defaults to 'png'
        :type extension: str, optional
        :param no_axis: whether to remove axis when saving the figure, defaults to True
        :type no_axis: bool, optional
        """
        filepath = os.path.join(path, f'{name}.{extension}')
        self._log_service.log_debug(f'Saving plot figure to filesystem [filepath: \'{filepath}\']')
        if fig is not None:
            fig.savefig(filepath, bbox_inches='tight')
        else:
            plt.savefig(filepath, bbox_inches='tight')

    def set_date_stamp(self, addition="") -> List[str]:
        """generates printable date stamp

        :param addition: if an addition should be put to the back of the generated date stamp, defaults to ""
        :type addition: str, optional
        :raises Exception: if stamp is already loaded, exception will be thrown
        :return: the generated date stamp
        :rtype: List[str]
        """
        if (len(self.stamp) > 2):
            raise Exception(
                "Attempting to reset datestamp, but it was already set")

        self.actual_date = datetime.now()
        self.stamp = str(self.actual_date).split(".")[0].replace(
            " ", "_").replace(':', '.') + addition
        print(f"Made datestamp: {self.stamp}")
        return self.stamp
