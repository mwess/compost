"""
Put everything together here.
"""
from tokenizers.abstracttokenizer import load_tokenizer, load_data
from taggers.abstracttagger import load_taggers
from src.job import Job

DEFAULT_SAVE_PATH = '.'

TRAIN_MODE = 'train'
TAG_MODE = 'tag'
TRAIN_KFCV = 'kfcv'

class Pipeline():

    DEFAULT_PARSER = "NLTKTokenizer"

    def __init__(self):
        self._tokenizer = None
        self._jobs = []


    def execute_options(self, options):
        self._load_tokenizer()
        self._load_taggers()
        data_read_mode = options.opts.get('input_mode', None)
        self._data = load_data(self._tokenizer, options.opts['input_data'], data_read_mode, options.opts['mode'])
        if options.opts["mode"] == TRAIN_MODE:
            for job in self._jobs:
                job.train(self._data)
                job.save(options.opts.get('savepath', DEFAULT_SAVE_PATH))
        if options.opts["mode"] == TAG_MODE:
            for job in self._jobs:
                job.tag(self._data)
            self.write_output(options.opts['outputpath'])
        if options.opts["mode"] == TRAIN_KFCV:
            # Training with kfold cross validation.
            pass

    def _load_tokenizer(self, options):
        tokenizer_name = options.opts.get("tokenizer", Pipeline.DEFAULT_PARSER)
        self._tokenizer = load_tokenizer(tokenizer_name)

    def _load_taggers(self, options):
        tagger_list = options.opts["taggers"]
        taggers = load_taggers(tagger_list)
        self._jobs = []
        for key in taggers.keys():
            self._jobs.append(Job(taggers[key], options))

    def write_output(self, outpath):
        with open(outpath, 'w') as f:
            # First write header.
            header_str = "Word"
            for job in self._jobs:
                header_str += '\t' + job.name
            header_str += '\n'
            f.write(header_str)
            for i in range(len(self._data)):
                out_str = self._data[i]
                for job in self._jobs:
                    out_str += '\t' + job.result_tags[i]
                out_str += '\n'
                f.write(out_str)