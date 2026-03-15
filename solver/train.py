import os, sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from filters import WordleFilter


class WordleTrain:

    def __init__(self):
        pass

    # Finds bits gained for current guess
    # I = -log2(1/p(x))
    # p(x) = words remaining / total words (wordlist length)
    def information(self):
        pass

    # Finds expected value (information entropy) for guess
    # i.e Average information gained for a particular guess
    # E(I) = Sumof (p(x)) * log2(1/p(x))
    def entropy(self):
        pass

    # Might not be needed
    # finds all combinations for a guess
    def combinations(self):
        pass

    # Gets entropy values for every word as a first guess
    def find_first_guess(self):
        pass