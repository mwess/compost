from itertools import groupby
import os
import shutil
import subprocess
from taggers.abstracttagger import AbstractTagger


def build_lexicon(train_data):
    # Tokens in the training data usually have the form: (token, tag).
    fl = [token for sublist in train_data for token in sublist]
    lexicon = []
    for k, g in groupby(fl, key=lambda x: x[0]):
        lexicon.append((k, list(g)))
    return lexicon


def extractTagSet(sentencelist):
    return list(set([token[1] for sentence in sentencelist for token in sentence]))


class Tagger(AbstractTagger):

    def __init__(self):
        self._model_name = "treetagger"
        self._input_filename = 'input'
        self._output_filename = 'output'
        self._tagset_filename = 'tagset'
        self._lexicon_filename = 'lexicon'
        self._treetagger_command = ''
        self._temp_path = None
        self._temp_model_path = None

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
        punctuationtag = "$."
        tagset = extractTagSet(trainset)
        tagset_file = os.path.join(self._temp_path, self._tagset_filename)
        with open(tagset_file, 'w') as f:
            f.write(" ".join(tagset))
        lexicon = build_lexicon(trainset)
        lexicon_file = os.path.join(self._temp_path, self._lexicon_filename)
        with open(lexicon_file) as f:
            for entry in lexicon:
                line = entry[0] + '\t' + ' -\t'.join(set(entry[1])) + '\n'
                f.write(line)
        input_file = os.path.join(self._temp_path, self._input_filename)
        if os.path.exists(input_file):
            os.remove(input_file)
        with open(input_file, 'w') as f:
            for sentence in trainset:
                for token in sentence:
                    f.write('\t'.join(token) + '\n')
                f.write('\n')
        subprocess.run("train-tree-tagger -st %s %s %s %s %s > /dev/null " %(punctuationtag,
                                                                             lexicon_file,
                                                                             tagset_file,
                                                                             input_file,
                                                                             self._temp_path),
                       shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

    def tag(self, data):
        # Why punctuationtag here?
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
        #now merge correct_result
        with open(output_file) as f:
            result  = f.readlines()
        return list(zip(data, result))

    def requires_additional_params(self):
        return True
