import os
import shutil
import subprocess
from taggers.abstracttagger import AbstractTagger
# from src.util.Formatparser import Formatparser

def extractTagSet(sentencelist):
    tagset = []
    for i,sentence in enumerate(sentencelist):
        for pair in sentence:
        #get tag from training
            tagset.append(pair[1])
    return list(set(tagset))

class Tagger(AbstractTagger):

    def __init__(self):
        self._model_name = "treetagger"
        self._input_filename = 'input'
        self._output_filename = 'output'
        self._tagset_filename = 'tagset'
        self._lexicon_filename = 'lexicon'
        self._treetagger_command = ''
        pass

    @property
    def model_name(self):
        return self._model_name

    def save(self, fpath):
        savepath = os.path.join(fpath, self.model_name)

    def load(self, fpath):
        loadpath = os.path.join(fpath, self.model_name)

    def add_temp_dir(self, temp_path):
        self._temp_path = temp_path
        self._temp_model_path = os.path.join(self._temp_path, self.model_name)
        if not os.path.exists(self._temp_path):
            os.mkdir(self._temp_path)

    def save(self, path):
        spath = os.path.join(path, self.model_name)
        shutil.move(self._temp_model_path, spath)

    def load(self, path):
        lpath = os.path.join(path, self.model_name)
        shutil.copy(lpath, self._temp_path)


    def __del__(self):
        shutil.rmtree(self._temp_path)

    def train(self, trainset):
        tagset = extractTagSet(trainset)
        tagset_file = os.path.join(self._temp_path, self._tagset_filename)
        with open(tagset_file, 'w') as f:
            f.write(" ".join(list(set(tagset))))
            punctuationtag = "$."

        lexicon = Formatparser.buildTreetaggerLexicon(trainset)
        lexicon_file = os.path.join(self._temp_path, self._lexicon_filename)
        with open(lexicon_file) as f:
            f.write(Formatparser.lexiconTreetaggerString(lexicon))
        inputfile = Formatparser.buildTreetaggerTrainingString(trainset)
        input_file = os.path.join(self._temp_path, self._input_filename)
        if os.path.exists(input_file):
            os.remove(input_file)
        with open(input_file, 'w') as f:
            f.write(inputfile)
        subprocess.run("train-tree-tagger -st %s %s %s %s %s > /dev/null " %(punctuationtag,
                                                                             lexicon_file,
                                                                             tagset_file,
                                                                             input_file,
                                                                             self._temp_path),
                       shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

    def tag(self, data):
        # Why punctuationtag
        punctuationtag = "$."
        input_file = os.path.join(self._temp_path, self._input_filename)
        output_file = os.path.join(self._temp_path, self._output_filename)
        model_file = os.path.join(self._temp_path, self._model_name)
        with open(input_file, 'w') as f:
            f.write('\n'.join(data))
        subprocess.run("tree-tagger %s %s %s" %(model_file,
                                                input_file,
                                                output_file),
                       shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        #now merge result
        with open(output_file) as f:
            result  = f.readlines()
        self._result = list(zip(data, result))

    def requires_additional_params(self):
        return True
