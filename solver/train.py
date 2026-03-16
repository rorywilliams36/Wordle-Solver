import os, sys
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from filters import WordleFilter
from wordle_game import WordleGame

WORD_LIST = sorted(set(np.loadtxt("data/wordlists/answer_wordlist.txt", dtype=str))) # All words available in wordle
WORD_LIST_LEN = len(WORD_LIST)
MAX_GUESSES = 6

PATH = 'C:/Users/roryw/Documents/Wordle Solver/data'

class WordleTrain:
    def __init__(self):
        self.guess_matrix = None
        self.word_to_index = None

    def entropy(self, pattern_counts):
        '''
        Finds expected value (information entropy) for guess
        i.e Average information gained for a particular guess
        H = - (Sumof [(p(x)) * log2(p(x))])

        Args:
            pattern_counts: dict containing counters for occurences of each result/pattern

        Returns:
            Entropy value (int)
        '''
        H = 0
        counts = pattern_counts.values()
        total = sum(counts)
        for count in counts:
            p = count / total
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
        with open(f"{PATH}/guess_matrix.npy", 'wb') as f:
            np.save(f, m)

    def find_first_guess(self):
        '''
        Calculates the expected information gained for every word as a first guess
        '''

        guess_matrix, word_to_index = load_lookup_table()

        guess_entropy = dict()

        for guess in WORD_LIST:
            pattern_counts = dict()
            for answer in WORD_LIST:
                # Lookup result for guess and answer
                g_idx = word_to_index[guess]
                a_idx = word_to_index[answer]
                res = guess_matrix[g_idx][a_idx]

                # Increment result occurence
                if pattern_counts.get(res):
                    pattern_counts[res] += 1
                else:
                    pattern_counts[res] = 1

            # Calculate entropy for word
            H = self.entropy(pattern_counts)
            guess_entropy[guess] = H

        # Save values as JSON
        with open(f"{PATH}/first_guess_entropy.json", "w") as f:
            json.dump(guess_entropy, f)             

    def solve(self, first_guess: str = None):
        '''
        Plays every possible Wordle game using a set word as the first guess

        Args:
            first_guess: str word to be set as the inital guess

        return:
            avg number of guesses for the game
        '''

        filters = WordleFilter(WORD_LIST)

        # Load data
        guess_matrix, word_to_index = load_lookup_table()
        first_guesses = load_first_guess_entropy()

        # Set first guess
        if (first_guess is None) or (not first_guesses.get(guess)):
            first_guess = max(first_guesses, key = first_guesses.get)

        num_guesses = []
        for answer in list(WORD_LIST)[:50]:
            guess = first_guess
            guess_num = 1
            solved = False
            print('================')
            print(answer)

            # Set containing all submitted guesses
            # avoids same guess being submitted if contains the same letters
            # as answer but in differnet order
            completed_guesses = set()

            while (not solved):
                if guess_num > MAX_GUESSES:
                    solved = True
                    guess_num = -2

                # gets result for chosen guess
                g_idx = word_to_index[guess]
                a_idx = word_to_index[answer]
                res = guess_matrix[g_idx][a_idx]

                print(guess_num, guess)

                # Set guess as submitted 
                completed_guesses.add(guess)
                if guess == answer:
                    solved = True
                else:
                    # finds possible guesses based on the result
                    filters.grey, filters.yellow, filters.green = filters.allocate_letters(guess, res)
                    _, pos_guesses = filters.filter()
                    pos_guesses = pos_guesses - completed_guesses

                    # checks if there are any guesses to be made
                    if len(pos_guesses) > 0:
                        guess = self.possible_guess_entropy(pos_guesses, guess_matrix, word_to_index)
                    # if no guesses available set to unsolved
                    else:
                        solved = True
                        guess_num = -2
    
                guess_num += 1      
     
            num_guesses.append(guess_num)
            filters.__init__(words=WORD_LIST)
        print(num_guesses)
        print(np.mean(num_guesses))

    def possible_guess_entropy(self, pos_guesses, guess_matrix, word_to_index):
        ''' Gets all possible patterns for result '''
        pos_guess_entropy = dict()
        # print(pos_guesses)
        for guess in pos_guesses:
            pattern_counts = dict()
            for answer in pos_guesses:
                # Lookup result for guess and answer
                g_idx = word_to_index[guess]
                a_idx = word_to_index[answer]
                res = guess_matrix[g_idx][a_idx]

                # Increment result occurence
                if pattern_counts.get(res):
                    pattern_counts[res] += 1
                else:
                    pattern_counts[res] = 1

            # Calculate entropy for word
            H = self.entropy(pattern_counts)
            pos_guess_entropy[guess] = H
        # print(pos_guess_entropy)
        return max(pos_guess_entropy, key = pos_guess_entropy.get)

def load_lookup_table():
    # Load guess lookup matrix
    guess_matrix = np.load(f"{PATH}/guess_matrix.npy", allow_pickle=True).tolist()
    word_to_index = {w:i for i,w in enumerate(WORD_LIST)} # Indexing table for each word
    return guess_matrix, word_to_index

def load_first_guess_entropy():
    with open(f"{PATH}/first_guess_entropy.json", "r") as f:
        first_guesses = json.load(f)
    return first_guesses

if __name__ == "__main__":
    train = WordleTrain()

    # first_guess = load_first_guess_entropy()
    # print(first_guess['irate'])
    # print(max(first_guess, key = first_guess.get))
    train.solve()

    # train.lookup_table()
    # print('guess matrix complete')
    # train.find_first_guess()
    # print('first guesses complete')
