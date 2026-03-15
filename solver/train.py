import os, sys
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
        
        m = [['']*WORD_LIST_LEN for _ in range(WORD_LIST_LEN)]
        wordle = WordleGame()

        for g, guess in enumerate(list(WORD_LIST)):
            for a, answer in enumerate(list(WORD_LIST)):
                m[g][a] = "".join(wordle.pattern(guess, answer))

        np.save(f"{PATH}/guess_matrix.npy", m)


            
if __name__ == "__main__":
    train = WordleTrain()
    guess_matrix = np.load("data/guess_matrix.npy", allow_pickle=True)
    print(guess_matrix)