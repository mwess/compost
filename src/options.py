from abc import ABC, abstractmethod, abstractproperty
import os
from src.utils import not_implemented

class AbstractOptions(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def parse_options(self):
        pass

    @abstractmethod
    @property
    def opts(self):
        pass



class OptionsFile(AbstractOptions):

    COMMENT_CHAR = "#"
    SPLIT_CHAR = "="

    def __init__(self, filepath):
        if not os.path.isfile(filepath):
            raise FileNotFoundError("File %s is not found." %filepath)
        self._filepath = filepath
        self._opts = {}
        self.parse_options()

    def parse_options(self):
        with open(self._filepath) as f:
            for line in f:
                if len(line) == 0 or line.startswith(OptionsFile.COMMENT_CHAR):
                    continue
                opt = line.split(maxsplit=1)
                if len(opt) != 2:
                    pass
                self._opts[opt[0]] = opt[1]

    def process_options(self):
        if "taggers" in self._opts:
            self._opts["taggers"] = self._opts["taggers"].split(",")


    @property
    def opts(self):
        return self._opts


@not_implemented
class XMLOptions(AbstractOptions):

    def __init__(self):
        pass

    def parse_options(self):
        pass