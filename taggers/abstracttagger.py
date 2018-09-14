from abc import ABC, abstractmethod
import importlib
import inspect
import os

from src.utils import deprecated

tagger_directory = "taggers"
default_taggerclass = "Tagger"


def load_taggers(tagger_list):
    """
    Load taggers from list. Currently only modules in tagger_directory are saved.
    :param tagger_list:
    :return: list of taggers.
    """
    taggers = []
    for module_name in tagger_list:
        available_modules = [x.split('.')[0] for x in os.listdir(tagger_directory)]
        if module_name not in available_modules:
            continue
        module = importlib.import_module('.'.join([tagger_directory, module_name]))
        tagger = getattr(module, default_taggerclass)
        if not inspect.isclass(tagger):
            raise Exception("Tagger %s is not a class!")
        taggers.append(tagger())
    return taggers


@deprecated
def load_tagger(tagger_name):
    module_name = tagger_name + ".py"
    if module_name not in os.listdir(tagger_directory):
        raise TaggerNotFoundException("%s not found." % tagger_name)
    module = importlib.import_module(os.path.join(tagger_directory, module_name))
    tagger = getattr(module, default_taggerclass)
    if not inspect.isclass(tagger):
        raise Exception("Tagger %s is not a class!")
    return tagger


class TaggerNotFoundException(Exception):
    pass


class AbstractTagger(ABC):
    """
    AbstractTagger class. All taggers in compost must inherit from this class in order to be callable.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    def save(self, fpath):
        mpath = os.path.join(fpath, self.model_name)
        self._save_model(mpath)
        """
        Save trained model in the given directory.
        :param fpath: directory to save path.
        :return:
        """
        pass

    @abstractmethod
    def _save_model(self, mpath):
        """
        Save trained model to given file path.
        :param mpath:
        :return:
        """
        pass

    def load(self, fpath):
        mpath = os.path.join(fpath, self.model_name)
        self._load_model(mpath)
        """
        Load model from path.
        :param fpath: directory of model to be loaded.
        :return: Model
        """
        pass

    @abstractmethod
    def _load_model(self, mpath):
        """
        Load model from file path.
        :param mpath:
        :return:
        """

    @abstractmethod
    def tag(self, data):
        """
        Part-Of-Speech tag a given sequence of data.
        :param data: list of tokens
        :return: list of tags
        """
        pass

    @abstractmethod
    def train(self, data):
        """
        Traing a Part-Of-Speech tagger model from data.
        :param data: list of tuples. Tuples have the form (token, tag)
        :return:
        """
        pass

    @property
    @abstractmethod
    def produces_temp_data(self):
        """
        Indicates if the inheriting tagger class requires additional storage for temporary data.
        :return: bool
        """
        pass

    @abstractmethod
    def add_temp_dir(self, temp_path):
        """
        Path to the temporary directory. Only called when produces_temp_data returns True.
        :param temp_path:
        :return:
        """
        pass

    @property
    @abstractmethod
    def requires_additional_params(self):
        """
        Return True if additional parameters are required for inheriting tagger class to be configured properly.
        :return: bool
        """
        pass

    @abstractmethod
    def set_additional_params(self, options):
        """
        Additional parameters for the tagger configuration can be passed here.
        :param options:
        :return:
        """
        pass

    @property
    @abstractmethod
    def model_name(self):
        """
        Name of model to be saved.
        :return: string
        """
        pass

    @property
    @abstractmethod
    def name(self):
        """
        Name of the tagger.
        :return: string
        """
        pass
