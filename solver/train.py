import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

from solver.filters import WordleFilter
import solver.data_utils as d_utils

MAX_GUESSES = 6

# File path and Names
PATH = f'{os.path.abspath(os.getcwd())}/data'
GUESS_ENTROPYS = 'first_guess_entropy'
WORD_PROBS = 'word_probabilites'


class WordleSolver:
    def __init__(self, guess_matrix, word_to_index, first_guess_entropy, word_probs, word_list):
        self.guess_matrix = guess_matrix
        self.word_to_index = word_to_index
        self.first_guess_entropy = first_guess_entropy
        self.word_probs = word_probs
        self.word_list = word_list

    
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
        guess_distribution = [0,0,0,0,0,0,0]
        for answer in list(self.word_list):
            filters = WordleFilter(self.word_list)

            guess = first_guess
            entropy = self.first_guess_entropy[guess]
            pos_guesses_remain = len(self.word_list)
            guess_num = 0
            solved = False
            # print('================')
            # print(answer)

            # Set containing all submitted guesses
            # avoids same guess being submitted if contains the same letters
            # as answer but in differnet order
            completed_guesses = set()

            guess_record[answer] = []

            while (not solved) or (guess_num < MAX_GUESSES):
                guess_num += 1

                max_entropy = -np.log2(1/pos_guesses_remain)      

                # gets result for chosen guess
                g_idx = self.word_to_index[guess]
                a_idx = self.word_to_index[answer]
                res = self.guess_matrix[g_idx][a_idx]
                # print(guess_num, guess, res, entropy, pos_guesses_remain)
                guess_record[answer].append((guess_num, guess, res, entropy, pos_guesses_remain))

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
                    pos_guess_entropys = self.possible_guess_entropy(pos_guesses, max_entropy)
                    guess = max(pos_guess_entropys, key = pos_guess_entropys.get)
                    entropy = pos_guess_entropys[guess]
                    pos_guesses_remain = len(pos_guesses)
                    #print(max_entropy)
                    
                # if no guesses available set to unsolved
                else:
                    break
         
            num_guesses.append(guess_num)
            if guess_num <=6:
                guess_distribution[guess_num-1] += 1
            else:
                solved = True
                guess_distribution[-1] += 1
                print(answer)
                print(guess_record[answer])
                print('========================')

        # print(num_guesses)
        print(guess_distribution)
        print(np.mean(num_guesses))

    def possible_guess_entropy(self, pos_guesses, max_entropy):
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
            H = entropy(pattern_counts)
            if not self.word_probs.get(guess):
                word_prob = self.word_probs['pupal'] * 0.1
            else:
                word_prob = self.word_probs[guess]

            score = expected_score(H, word_prob, max_entropy)
            # print(guess, H, score, max_entropy, word_prob)
            pos_guess_entropy[guess] = score

        return pos_guess_entropy


def entropy(pattern_counts):
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

def expected_score(H, word_prob, max_entropy):
    entropy_ratio = H / max_entropy
    return entropy_ratio +  word_prob

# Main Functions
def run_gather_data(word_list):
    ''' Runs functions used to create/calculate the data needed to run solver'''
    solver = WordleSolver(None, {}, {}, {}, word_list)
    d_utils.create_guess_matrix(word_list)
    guess_matrix, word_to_index = d_utils.load_guess_matrix(word_list)
    d_utils.find_first_guess(word_list, word_to_index, guess_matrix)
    d_utils.apply_sigmoid()

def run_solver(word_list, first_guess):
    guess_matrix, word_to_index = d_utils.load_guess_matrix(word_list)
    first_guess_entropy = d_utils.load_json(GUESS_ENTROPYS)
    word_probs = d_utils.load_json(WORD_PROBS)

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