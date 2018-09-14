import os

import dill
from nltk.tag.perceptron import PerceptronTagger

from taggers.abstracttagger import AbstractTagger


class Tagger(AbstractTagger):

    def __init__(self):
        self._tagger = PerceptronTagger(load=False)
        self._name = 'nltkperceptron'
        self._model_name = "nltkperceptron"
        self._result = None
        super().__init__()

    def _save_model(self, fpath):
        with open(fpath, 'wb') as f:
            dill.dump(self._tagger, f)

    def load(self, path):
        if path == '':
            self._load_model(path)
        else:
            mpath = os.path.join(path, self.model_name)
            self._load_model(mpath)

    def _load_model(self, fpath):
        if fpath == '':
            self._tagger = PerceptronTagger(load=True)
        else:
            with open(fpath, 'rb') as f:
                self._tagger = dill.load(f)

    def tag(self, data):
        res = self._tagger.tag(data)
        return [x[1] for x in res]

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

    @property
    def name(self):
        return self._name
