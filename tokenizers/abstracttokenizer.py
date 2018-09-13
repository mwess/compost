from abc import ABC, abstractmethod
import importlib
import inspect
import os


default_classname = "Tokenizer"
tokenizer_directory = "tokenizers"

def load_tokenizer(tokenizer_name):
    module_name = tokenizer_name + ".py"
    if module_name not in os.listdir(tokenizer_directory):
        raise Exception("Tokenizer cannot be found.")
    tokenizer_module = importlib.import_module(os.path.join(tokenizer_directory, module_name))
    tokenizer = getattr(tokenizer_module, default_classname)
    if not inspect.isclass(tokenizer):
        raise Exception("Tokenizer class is missing!")
    return tokenizer()


def load_data(fpath, mode):
    # If fpath points to a directory we assume that each file in the directory should be loaded.
    pass


class AbstractTokenizer(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def tokenize(self, text):
        pass
