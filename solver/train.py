import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

from solver.filters import WordleFilter
import solver.load_data as _load

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from wordle_game import WordleGame

WORD_LIST = sorted(set(np.loadtxt("data/wordlists/answer_wordlist.txt", dtype=str)))
WORD_LIST_LEN = len(WORD_LIST)
MAX_GUESSES = 6

PATH = f'{os.path.abspath(os.getcwd())}/data'

class WordleSolver:
    def __init__(self, guess_matrix, word_to_index, first_guess_entropy, word_probs, word_list: set = WORD_LIST):
        self.guess_matrix = guess_matrix
        self.word_to_index = word_to_index
        self.first_guess_entropy = first_guess_entropy
        self.word_probs = word_probs
        self.word_list = word_list

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
    
    def create_guess_matrix(self):
        '''
        Creates matrix where matrix[guess][answer] is the comparison of words using 
        wordle game logic
        Matrix is saved and saves time since the comparisons between guesses and answers never change
        '''

        # Initalise matrix
        word_list_len = len(self.word_list)
        guess_matrix = np.empty((word_list_len, word_list_len), dtype=np.dtype('U100'))
        wordle = WordleGame()

        word_list = list(self.word_list)

        # Fill matrix
        for g, guess in enumerate(word_list):
            for a, answer in enumerate(word_list):
                res = "".join(wordle.pattern(guess, answer))
                guess_matrix[g][a] = res

        guess_matrix_path = f'{PATH}/guess_matrix.npy'
        try:
            with open(guess_matrix_path, 'wb') as f:
                np.save(f, guess_matrix)
                f.close()
        except Exception as e:
            print(f"Error: {e}")

    def find_first_guess(self):
        '''
        Calculates the expected information gained for every word as a first guess
        '''

        guess_entropy = {}

        for guess in WORD_LIST:
            pattern_counts = {}
            for answer in WORD_LIST:
                # Lookup result for guess and answer
                g_idx = self.word_to_index[guess]
                a_idx = self.word_to_index[answer]
                res = self.guess_matrix[g_idx][a_idx]

                # Increment result occurence
                if pattern_counts.get(res):
                    pattern_counts[res] += 1
                else:
                    pattern_counts[res] = 1

            # Calculate entropy for word
            H = self.entropy(pattern_counts)
            guess_entropy[guess] = H

        entropy_file_path = f"{PATH}/first_guess_entropy.json"

        # Save values as JSON
        try:
            with open(entropy_file_path, 'w') as f:
                json.dump(guess_entropy, f)
        except Exception as e:
            print(f'Error: {e}')

    def solve(self, first_guess: str = None):
        '''
        Plays every possible Wordle game using a set word as the first guess

        Args:
            first_guess: str word to be set as the inital guess

        return:
            avg number of guesses for the game
        '''


        # Set first guess if none is defined
        if (first_guess is None) or (not self.first_guess_entropy.get(first_guess)):
            first_guess = max(self.first_guess_entropy, key = self.first_guess_entropy.get)

        num_guesses = []
        guess_record = {}
        guess_distribution = [0,0,0,0,0,0]
        for answer in list(WORD_LIST)[:10]:
            filters = WordleFilter(WORD_LIST)

            guess = first_guess
            entropy = self.first_guess_entropy[guess]
            pos_guesses_remain = len(self.word_list)
            guess_num = 0
            solved = False
            print('================')
            print(answer)

            # Set containing all submitted guesses
            # avoids same guess being submitted if contains the same letters
            # as answer but in differnet order
            completed_guesses = set()

            guess_record[answer] = []

            while (not solved) or (guess_num < MAX_GUESSES):
                guess_num += 1      

                # gets result for chosen guess
                g_idx = self.word_to_index[guess]
                a_idx = self.word_to_index[answer]
                res = self.guess_matrix[g_idx][a_idx]
                print(self.guess_matrix)
                print(guess_num, guess, res, entropy, pos_guesses_remain)
                # guess_record[answer].append((guess_num, guess))

                # Set guess as submitted 
                completed_guesses.add(guess)
                if guess == answer:
                    solved = True
                    break
                
                # finds possible guesses based on the result
                filters.grey, filters.yellow, filters.green = filters.allocate_letters(guess, res)
                _, pos_guesses = filters.filter()
                pos_guesses = pos_guesses - completed_guesses

                # checks if there are any guesses to be made
                # Gets the word to be guesses next
                if len(pos_guesses) > 0:
                    pos_guess_entropys = self.possible_guess_entropy(pos_guesses)
                    guess = max(pos_guess_entropys, key = pos_guess_entropys.get)
                    entropy = pos_guess_entropys[guess]
                    pos_guesses_remain = len(pos_guesses)
                # if no guesses available set to unsolved
                else:
                    break
         
            num_guesses.append(guess_num)
            if guess_num <=6:
                guess_distribution[guess_num-1] += 1
        print(num_guesses)
        print(guess_distribution)
        print(np.mean(num_guesses))

    def possible_guess_entropy(self, pos_guesses):
        ''' 
        Calculates entropy values for all possible guesses left

        Args:
            pos_guesses: set of words that are possible answers/gueses

        Returns:
            pos_guess_entropy: dict containing entropy values for the possible guesses
        '''
        pos_guess_entropy = {}
        # print(pos_guesses)
        for guess in pos_guesses:
            pattern_counts = {}
            for answer in pos_guesses:
                # Lookup result for guess and answer
                g_idx = self.word_to_index[guess]
                a_idx = self.word_to_index[answer]
                res = self.guess_matrix[g_idx][a_idx]

                # Increment result occurence
                if pattern_counts.get(res):
                    pattern_counts[res] += 1
                else:
                    pattern_counts[res] = 1

            # Calculate entropy for word
            H = self.entropy(pattern_counts)
            pos_guess_entropy[guess] = H

        return pos_guess_entropy


def apply_sigmoid():
    ''' Applies sigmoid function to wordlist to calculate a probability for word being the answer '''

    # open wordlist
    try:
        with open(f"{PATH}/wordlists/words.txt", "r") as f:
            most_likely = f.readlines()
            f.close()
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error: {e}')


    # Apply sigmoid function (z)
    most_likely.reverse()
    most_likely_len = len(most_likely)
    x = np.linspace(-5, 10, most_likely_len)
    z = 1/(1 + np.exp(-x))

    # Attach sigmoid value to words
    word_prob = {}
    for w in range(most_likely_len):
        word = most_likely[w].strip()
        word_prob[word] = z[w]

    # Save values
    word_prob_path = f"{PATH}/word_probabilites.json"
    try:
        with open(word_prob_path, 'w') as f:
            json.dump(word_prob, f)
    except Exception as e:
        print(f'Error: {e}')

# Main Functions
def run_gather_data(word_list):
    solver = WordleSolver(None, {}, {}, word_list)
    solver.create_guess_matrix()
    solver.first_guess_entropy

def run_solver(word_list, first_guess):
    guess_matrix, word_to_index = _load.load_guess_matrix(word_list)
    first_guess_entropy = _load.load_first_guess_entropy()
    word_probs = _load.load_word_probs()

    if (len(guess_matrix) == 0) or (len(first_guess_entropy) == 0) or (len(word_probs) == 0):
        print('Error loading data')
        sys.exit()
        
    solver = WordleSolver(guess_matrix, word_to_index, first_guess_entropy, word_probs, word_list)
    solver.solve(first_guess)


if __name__ == "__main__":
    # guess_matrix, word_to_index = load_guess_matrix()
    # first_guess_entropy = load_first_guess_entropy()

    # if (len(guess_matrix) == 0) or (len(first_guess_entropy) == 0):
    #     print('Error loading data')
        
    train = WordleTrain(guess_matrix, word_to_index, first_guess_entropy)
    train.solve()