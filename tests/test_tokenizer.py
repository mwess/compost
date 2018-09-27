"""
Perform tests for tokenizers here.
"""
import unittest
from compost.options import OptionsFile
from tokenizers.abstracttokenizer import load_tokenizer, TokenizerNotFoundException, TokenizerClassMissingException
try:
    import nltk
    NLTK_IMPORTED=True
except ModuleNotFoundError:
    NLTK_IMPORTED=False

class TokenizerTests(unittest.TestCase):

    def setUp(self):
        if not NLTK_IMPORTED:
            self.skipTest("NLTK library could not be imported.")

    def test_nltk(self):
        text = "This is a simple test to test the nltk tokenizer."
        text_tokens = nltk.word_tokenize(text)
        option = OptionsFile('tests/additional_data/tokenizer_test_case_1_options')
        tokenizer = load_tokenizer(option.opts['tokenizer'])()
        self.assertListEqual(text_tokens, tokenizer.tokenize(text))

    def test_tokenizer_not_found(self):
        self.assertRaises(TokenizerNotFoundException, load_tokenizer, 'SomeNonExistentTokenizer')

    def test_missing_class(self):
        self.assertRaises(TokenizerClassMissingException, load_tokenizer, 'dummytokenizer')