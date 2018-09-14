import unittest
from src.io import load_data
try:
    from nltk import word_tokenize
    NLTK_IMPORTED = True
except ModuleNotFoundError:
    NLTK_IMPORTED = False


class IOTests(unittest.TestCase):

    def setUp(self):
        if not NLTK_IMPORTED:
            self.skipTest("NLTK could not be imported.")

    def test_io_dir(self):
        input_directory = 'tests/additional_data/io_test_case_1_inputdata'
        correct_solution = ['This', 'is', 'an', 'example', 'sentence', 'for', 'document1', '.', 'I',
                             'am', 'hungry', '.', 'How', 'is', 'the', 'weather', 'today', '?', 'Is',
                             'it', 'more', 'dry', 'or', 'more', 'wet', '?']
        program_mode = 'tag'
        file_type = 'txt'
        data = load_data(word_tokenize, input_directory, program_mode, file_type)
        self.assertListEqual(data, correct_solution)