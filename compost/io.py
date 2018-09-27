"""
Handles file reading and file storing.
"""
import os


def load_data(tokenizer_func, path, program_mode, file_type):
    """
    Function to load input data.
    :param tokenizer_func: Function to tokenize read strings.
    :param path: Path to input file or input directory.
    :param program_mode: Mode like 'train', 'tag', etc. Different modes sometines require different reader functions
    for the same file type.
    :param file_type: Additional argument if the file suffix is not a clear indicator for the reader function, i.e.
    we know different formats in xml files.
    :return: return a list of tokens for further processing.
    """
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
    """
    :param fname: Path to input file or input directory.
    :param program_mode: Mode like 'train', 'tag', etc. Different modes sometines require different reader functions
    for the same file type.
    :param file_type: Additional argument if the file suffix is not a clear indicator for the reader function, i.e.
    we know different formats in xml files.
    :return: reader function
    """
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


def read_file(tokenizer, fpath, program_mode, mode=None):
    """
    Use reader_function to read file. Text is not tokenized when the program_mode is not a training mode.
    :param tokenizer_func: Function to tokenize read strings.
    :param path: Path to input file or input directory.
    :param program_mode: Mode like 'train', 'tag', etc. Different modes sometines require different reader functions
    for the same file type.
    :param file_type: Additional argument if the file suffix is not a clear indicator for the reader function, i.e.
    we know different formats in xml files.
    :return: return a list of tokens for further processing.
    """
    read_func = get_filereader_function(fpath, program_mode, mode)
    if program_mode == "train":
        return read_func(fpath)
    else:
        return tokenizer().tokenize(read_func(fpath))


def read_txt_file(fpath):
    """
    Read file in txt format (no special structured format).
    :param fpath:
    :return:
    """
    with open(fpath) as f:
        text = f.read()
    return text


def read_training_txt_file(fpath):
    """
    Read training data in txt file format. Structure is: One token per line, seperated by '\t'. First element is
    token, second is tag.
    :param fpath:
    :return:
    """
    with open(fpath) as f:
        content = f.read().split('\n\n')
        sentences = [x.split('\n') for x in content]
        sentences = [[x.split('\t') for x in y] for y in sentences]
    return sentences


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


