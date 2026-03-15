import os, sys
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from filters import WordleFilter
from wordle_game import WordleGame

WORD_LIST = sorted(set(np.loadtxt("data/wordlists/answer_wordlist.txt", dtype=str))) # All words available in wordle
WORD_LIST_LEN = len(WORD_LIST)

PATH = 'C:/Users/roryw/Documents/Wordle Solver/data'

class WordleTrain:

    def __init__(self):
        pass

    # Finds expected value (information entropy) for guess
    # i.e Average information gained for a particular guess
    # E(I) = Sumof (p(x)) * log2(1/p(x))
    def entropy(self, pattern_counts):
        H = 0
        total = sum(pattern_counts.values())
        for c in pattern_counts.values():
            p = c / total
            if p > 0:
                H -= p * np.log2(p)

        return H
    
    def lookup_table(self):
        '''
        Creates matrix where matrix[guess][answer] is the comparison of words using 
        wordle game logic
        Matrix is saved and saves time since the comparisons between guesses and answers never change
        '''

        # Initalise matrix
        m = [['']*WORD_LIST_LEN for _ in range(WORD_LIST_LEN)]
        wordle = WordleGame()

        # Fill matrix
        for g, guess in enumerate(list(WORD_LIST)):
            for a, answer in enumerate(list(WORD_LIST)):
                m[g][a] = "".join(wordle.pattern(guess, answer))

        # Save matrix
        np.save(f"{PATH}/guess_matrix.npy", m)


    # Gets entropy values for every word as a first guess
    def find_first_guess(self):
        word_filters = WordleFilter()
        wordle = WordleGame()

        guess_matrix = np.load(f"{PATH}/guess_matrix.npy", allow_pickle=True).tolist()
        word_to_index = {w:i for i,w in enumerate(WORD_LIST)}

        guess_entropy = dict()

        for guess in WORD_LIST:
            pattern_counts = dict()
            for answer in WORD_LIST:
                g_idx = word_to_index[guess]
                a_idx = word_to_index[answer]

                res = guess_matrix[g_idx][a_idx]

                if pattern_counts.get(res):
                    pattern_counts[res] += 1
                else:
                    pattern_counts[res] = 1

                word_filters.__init__()

            H = self.entropy(pattern_counts)
            guess_entropy[guess] = H

        with open(f"{PATH}/first_guess_entropy.json", "w") as f:
            json.dump(guess_entropy, f)                

if __name__ == "__main__":
    train = WordleTrain()
    #guess_matrix = np.load("data/guess_matrix.npy", allow_pickle=True)
    with open(f"{PATH}/first_guess_entropy.json", "r") as f:
        first_guess = json.load(f)
    print(first_guess)
    #print(guess_matrix)