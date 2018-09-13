import dill
from nltk.tag.perceptron import PerceptronTagger
from taggers.abstracttagger import AbstractTagger


class Tagger(AbstractTagger):

    def __init__(self):
        self._tagger = PerceptronTagger(load=False)
        self._model_name = "nltkperceptron"
        self._result = None

    def save(self, fpath):
        with open(fpath, 'wb') as f:
            dill.dump(self._tagger, f)

    def load(self, fpath):
        with open(fpath, 'rb') as f:
            self._tagger = dill.load(f)

    def tag(self, data):
        self._result = self._tagger.tag(data)

    def train(self, data):
        # Reset tagger.
        self._tagger = PerceptronTagger(load=False)
        self._tagger.train(data)

    @property
    def produces_temp_data(self):
        return False

    @property
    def requires_additional_params(self):
        return False

    def set_additional_params(self, options):
        pass

    def add_temp_dir(self, options):
        pass

    @property
    def model_name(self):
        return self._model_name