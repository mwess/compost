import os
import unittest
from taggers.abstracttagger import load_taggers
from compost.options import OptionsFile
from compost.pipeline import Pipeline
try:
    from taggers.NLTKPerceptron import Tagger as perctagger
    from nltk import word_tokenize
    from nltk.tag.perceptron import PerceptronTagger
    NLTK_IMPORTED = True
except ModuleNotFoundError:
    NLTK_IMPORTED = False



class TaggerTests(unittest.TestCase):

    def setUp(self):
        if not NLTK_IMPORTED:
            self.skipTest("nltk could not be imported.")

    def test_perceptron_tagging(self):
        sentence = "This is a test sentence to test if the testing works."
        tokens = word_tokenize(sentence)
        pt = PerceptronTagger(load=True)
        tag_result1 = [x[1] for x in pt.tag(tokens)]
        pt2 = perctagger()
        pt2.load()
        tag_result2 = pt2.tag(tokens)
        self.assertListEqual(tag_result1, tag_result2)

    def test_perceptron_training(self):
        option_file1 = 'tests/additional_data/train_test_1_option'
        option_file2 = 'tests/additional_data/train_test_1_option_load'
        opt1 = OptionsFile(option_file1)
        opt2 = OptionsFile(option_file2)
        p1 = Pipeline()
        p1.execute_options(opt1)
        p2 = Pipeline()
        p2.execute_options(opt2)
        if os.path.exists(opt2.opts['outputpath']):
            res = True
            os.remove(opt2.opts['outputpath'])
        self.assertTrue(res)
