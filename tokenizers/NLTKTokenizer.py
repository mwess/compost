from nltk import word_tokenize
from tokenizers.abstracttokenizer import AbstractTokenizer

class Tokenizer(AbstractTokenizer):

    def __init__(self, language='english'):
        self._language = language

    def tokenize(self, text):
        return word_tokenize(text, self._language)