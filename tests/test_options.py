"""
Formulate tests for the options module here.
"""
import os
import unittest
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from compost.options import OptionsFile


class OptionsFileTest(unittest.TestCase):

    def test_on_not_existens_file(self):
        filename = "somefilenamethatshouldnexists"
        self.assertRaises(FileNotFoundError, OptionsFile, filename)

    def test_working_file(self):
        filepath = 'tests/additional_data/optionstest2'
        correct_dict = {
            'mode': 'tag',
            'taggers': 'perceptron,hmm,crf,treetagger',
            'tokenizer': 'NLTKTokenizer',
            'input': 'somedirectory'
        }
        options = OptionsFile(filepath)
        self.assertDictEqual(options.opts, correct_dict)


if __name__ == "__main__":
    unittest.main()
