"""
Handle file reading and file storing here.
"""
import os
from src.utils import not_implemented


def load_data(tokenizer_func, path, program_mode, file_type):
    docs = []
    if not os.path.exists(path):
        raise FileNotFoundError("%s could not be found." %path)
    if os.path.isfile(path):
        docs.append(read_file(tokenizer_func, path, program_mode, file_type))
    else:
        for _, _, files in os.walk(path):
            for f in files:
                fp = os.path.join(path, f)
                docs.append(read_file(tokenizer_func, fp, program_mode, file_type))
    return [token for sentence in docs for token in sentence]


def get_filereader_function(fname, program_mode, mode=None):
    if mode is None:
        if '.' not in fname:
            reader_id = ''
        else:
            _, reader_id = fname.rsplit('.', maxsplit=1)
    else:
        reader_id = mode
    if program_mode == 'train':
        reader_id += "_train"
    return file_parse_dict[reader_id]


def read_file(tokenizer_func, fpath, program_mode, mode=None):
        read_func = get_filereader_function(fpath, program_mode, mode)
        if program_mode == "train":
            return read_func(fpath)
        else:
            return tokenizer_func().tokenize(read_func(fpath))


def read_txt_file(fpath):
    with open(fpath) as f:
        text = f.read()
    return text


def read_training_txt_file(fpath):
    with open(fpath) as f:
        content = [x.split() for x in f.readlines()]
    return content


def read_gutenberg(fpath):
    pass


def read_dwds(fpath):
    pass


def read_textgrid(fpath):
    pass


file_parse_dict = {
    '': read_txt_file,
    'txt': read_txt_file,
    '_train': read_training_txt_file,
    'txt_train': read_training_txt_file
}


