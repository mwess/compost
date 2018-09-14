from abc import ABC, abstractmethod
import importlib
import inspect
import os

tagger_directory = "taggers"
default_taggerclass = "Tagger"


def load_taggers(tagger_list):
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

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save(self, fpath):
        pass

    @abstractmethod
    def load(self, fpath):
        pass

    @abstractmethod
    def tag(self, data):
        pass

    @abstractmethod
    def train(self, data):
        pass

    @property
    @abstractmethod
    def produces_temp_data(self):
        pass

    @abstractmethod
    def add_temp_dir(self, options):
        pass

    @property
    @abstractmethod
    def requires_additional_params(self):
        pass

    @abstractmethod
    def set_additional_params(self, options):
        pass

    @property
    @abstractmethod
    def model_name(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass
