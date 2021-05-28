import os
import pickle

from nltk.tokenize import word_tokenize
from .train_classifier import remove_noise


def analyse_sentiment(text):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = os.path.join(__location__, 'classifier.sav')
    classifier = pickle.load(open(filename, 'rb'))
    custom_tokens = remove_noise(word_tokenize(text))
    return classifier.classify(dict([token, True] for token in custom_tokens))
