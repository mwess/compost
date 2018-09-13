from abc import ABC, abstractmethod
import os

class AbstractOptions(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def parse_options(self):
        pass

    @property
    @abstractmethod
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
                line = line.strip()
                if len(line) == 0 or line.startswith(OptionsFile.COMMENT_CHAR):
                    continue
                opt = line.split(OptionsFile.SPLIT_CHAR, maxsplit=1)
                if len(opt) != 2:
                    pass
                self._opts[opt[0]] = opt[1]

    def process_options(self):
        pass


    @property
    def opts(self):
        return self._opts


class XMLOptions(AbstractOptions):

    def __init__(self):
        pass

    def parse_options(self):
        pass
