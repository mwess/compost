import os
from uuid import uuid1
from taggers.abstracttagger import load_tagger

default_temporary_dir = "/tmp/compost"

class Job():

    def __init__(self, tagger, options):
        self._name = tagger.__name__
        self._tagger = tagger
        self._tagresult = None
        if self._tagger.produces_temp_data:
            self._init_temp_dir()
            self._tagger.add_temp_dir(self._temp_dir)
        if self._tagger.requires_additional_data:
            self._tagger.set_additional_params(options)

    def _init_temp_dir(self):
        temp_name = str(uuid1())
        self._temp_dir = os.path.join(default_temporary_dir, temp_name)
        if os.path.exists(self._temp_dir):
            # This should not happen.
            pass
        os.makedirs(self._temp_dir)

    def __del__(self):
        os.removedirs(self._temp_dir)

    def __str__(self):
        return self._name

    def train(self, data):
        self._tagger.train(data)

    def tag(self, data):
        self._tagresult =  self._tagger.tag(data)

    def save(self, path):
        self._tagger.save(path)

    def load(self, path):
        self._tagger.load(path)

    @property
    def result_tags(self):
        return self._tagresult

    @property
    def name(self):
        return self._name