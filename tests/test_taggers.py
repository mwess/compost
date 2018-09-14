import unittest
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

    def test_perceptron(self):
        sentence = "This is a test sentence to test if the testing works."
        tokens = word_tokenize(sentence)
        pt = PerceptronTagger(load=True)
        tag_result1 = pt.tag(tokens)
        pt2 = perctagger()
        pt2.load()
        pt2.tag(tokens)
        tag_result2 = pt2.result
        self.assertListEqual(tag_result1, tag_result2)