"""
Put everything together here.
"""
from tokenizers.abstracttokenizer import load_tokenizer
from taggers.abstracttagger import load_taggers
from compost.io import load_data
from compost.job import Job

DEFAULT_SAVE_PATH = '.'

TRAIN_MODE = 'train'
TAG_MODE = 'tag'
TRAIN_KFCV = 'kfcv'


class Pipeline:
    """
    Class that handles the execution of the program given an instance of Options. All modes are implemented here.
    """

    DEFAULT_PARSER = "NLTKTokenizer"

    def __init__(self):
        self._tokenizer = None
        self._jobs = []
        self._data = None

    def execute_options(self, options):
        """
        Uses options to exeute program.
        :param options:
        :return:
        """
        self._load_tokenizer(options)
        self._load_taggers(options)
        data_read_mode = options.opts.get('input_mode', None)
        self._data = load_data(self._tokenizer, options.opts['inputpath'], options.opts['mode'], data_read_mode)
        if options.opts["mode"] == TRAIN_MODE:
            for job in self._jobs:
                job.train(self._data)
                job.save(options.opts.get('savepath', DEFAULT_SAVE_PATH))
        if options.opts["mode"] == TAG_MODE:
            for job in self._jobs:
                job.load(options.opts['profilepath'])
                job.tag(self._data)
            self.write_output(options.opts['outputpath'])
        if options.opts["mode"] == TRAIN_KFCV:
            # Training with kfold cross validation.
            pass

    def _load_tokenizer(self, options):
        tokenizer_name = options.opts.get("tokenizer", Pipeline.DEFAULT_PARSER)
        self._tokenizer = load_tokenizer(tokenizer_name)

    def _load_taggers(self, options):
        tagger_list = options.opts["taggers"].split(',')
        taggers = load_taggers(tagger_list)
        self._jobs = []
        for tagger in taggers:
            self._jobs.append(Job(tagger, options))

    def write_output(self, outpath):
        with open(outpath, 'w') as f:
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
