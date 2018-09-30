import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import unittest
from compost.options import OptionsFile
from compost.pipeline import Pipeline
try:
    import nltk
    NLTK_IMPORTED = True
except ModuleNotFoundError:
    NLTK_IMPORTED = False

class CompostTest(unittest.TestCase):

    def setUp(self):
        if not NLTK_IMPORTED:
            self.skipTest("NLTK Could not be imported.")

    def test_compost_tagging_1(self):
        input_file = 'defaultoptions'
        options = OptionsFile(input_file)
        if os.path.exists(options.opts['outputpath']):
            os.remove(options.opts['outputpath'])
        pl = Pipeline()
        pl.execute_options(options)
        with open('tests/additional_data/compost_test/correct_result') as f:
            cr = f.read()
        with open(options.opts['outputpath']) as f:
            r = f.read()
        os.remove(options.opts['outputpath'])
        self.assertEqual(cr, r)

