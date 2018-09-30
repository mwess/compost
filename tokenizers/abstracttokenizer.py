from abc import ABC, abstractmethod
import importlib
import os


default_classname = "Tokenizer"
tokenizer_directory = "tokenizers"

def load_tokenizer(tokenizer_name):
    """
    Loads tokenizer from tokenizer_directory.
    :param tokenizer_name:
    :return:
    """
    module_name = tokenizer_name + ".py"
    if module_name not in os.listdir(tokenizer_directory):
        raise TokenizerNotFoundException("Tokenizer cannot be found.")
    tokenizer_module = importlib.import_module(tokenizer_directory + "." + tokenizer_name)
    try:
        tokenizer = getattr(tokenizer_module, default_classname)
    except AttributeError:
        raise TokenizerClassMissingException("Tokenizer class is missing!")
    return tokenizer


class TokenizerNotFoundException(Exception):
    pass

class TokenizerClassMissingException(Exception):
    pass


class AbstractTokenizer(ABC):
    """
    Class from which all tokenizers must inherit.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def tokenize(self, text):
        """
        Implementation of tokenizer function.
        :param text: Text to tokenize.
        :return:
        """
        pass
