import os
import sys
import time
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

        N = len(self.word_list)
        # Set first guess if none is defined
        first_entropy = 0
        if (first_guess is None) or (not self.first_guess_entropy.get(first_guess)):
            first_guess = max(self.first_guess_entropy, key = self.first_guess_entropy.get)
            first_entropy = self.first_guess_entropy[first_guess]

        num_guesses = []
        guess_record = {}
        guess_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # last idx is 10+/unsolved
        for i, answer in enumerate(list(self.word_list)[157:210]):
            filters = WordleFilter(self.word_list)

            guess = first_guess
            entropy = first_entropy
            pos_answers_remain = N
            guess_num = 0
            solved = False
            print('================')
            print(answer)

            # Set containing all submitted guesses
            # avoids same guess being submitted if contains the same letters
            # as answer but in differnet order
            completed_guesses = set()
            guess_record[answer] = []

            while (not solved):
                guess_num += 1

                max_entropy = -np.log2(1/pos_answers_remain)      

                # gets result for chosen guess
                g_idx = self.word_to_index[guess]
                a_idx = self.word_to_index[answer]
                res = self.guess_matrix[g_idx][a_idx]

                # add guess to record
                print(guess_num, guess, res, entropy, pos_answers_remain)
                guess_record[answer].append((guess_num, guess, res, entropy, pos_answers_remain))

                # Set guess as submitted 
                completed_guesses.add(guess)
                if guess == answer:
                    solved = True
                    break
                
                # finds possible guesses based on the result
                filters.grey, filters.yellow, filters.green = filters.allocate_letters(guess, res)
                pos_answers, allowed_guesses = filters.filter()
                pos_answers = pos_answers - completed_guesses
                allowed_guesses = set(allowed_guesses) - completed_guesses

                # checks if there are any guesses to be made
                # Gets the word to be guesses next
                if len(pos_answers) > 0:
                    pos_guess_scores = self.get_possible_guess_scores(pos_answers, allowed_guesses, max_entropy)
                    guess = max(pos_guess_scores, key = pos_guess_scores.get)
                    entropy = pos_guess_scores[guess]
                    pos_answers_remain = len(pos_answers)
                    #print(max_entropy)
                    
                # if no guesses available set to unsolved
                else:
                    break
         
            # record guess number
            num_guesses.append(guess_num)
            if guess_num <= 9:
                guess_distribution[guess_num-1] += 1
            else:
                solved = True
                guess_distribution[-1] += 1
                print(answer)
                print(guess_record[answer])
                print('========================')

            progress_bar(i, N)

        # print(num_guesses)
        print(guess_distribution)
        print(np.mean(num_guesses))

    def get_possible_guess_scores(self, pos_answers, allowed_guesses, max_entropy):
        ''' 
        Calculates entropy values for all possible guesses left

        Args:
            pos_answers: set of words that are possible answers

        Returns:
            pos_guess_entropy: dict containing entropy values for the possible guesses
        '''
        pos_guess_entropy = {}
        pos_guess_len = len(pos_answers)
        worst_word_prob = self.word_probs['pupal'] * 0.1
        # Change to all allowed guesses
        for guess in allowed_guesses:
            pattern_counts = {}

            # change to all possible answers
            for answer in pos_answers:
                # Lookup result for guess and answer
                pos_filtered = WordleFilter(pos_answers)

                # get result
                g_idx = self.word_to_index[guess]
                a_idx = self.word_to_index[answer]
                res = self.guess_matrix[g_idx][a_idx]

                # Increment result occurence
                pattern_counts[res] = pattern_counts.get(res, 0) + 1

            # Calculate entropy for word
            H = entropy(pattern_counts)
            worst_case = max(pattern_counts.values())

            # Get word probability
            # Add clause if word not in possible answers set word prob to 0
            if guess not in pos_answers:
                word_prob = 0
            elif not self.word_probs.get(guess):
                word_prob = worst_word_prob
            else:
                word_prob = self.word_probs[guess]

            # get score
            words_left_ratio = worst_case / pos_guess_len
            score = expected_score(H, word_prob, max_entropy, words_left_ratio)
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

def expected_score(H, word_prob, max_entropy, word_left):
    entropy_ratio = H / max_entropy
    return entropy_ratio +  word_prob - word_left

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

def progress_bar(current, total, bar_length=30):
    percent = current / total
    filled_length = int(bar_length * percent)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {current}/{total} words')
    sys.stdout.flush()

if __name__ == "__main__":
    # guess_matrix, word_to_index = load_guess_matrix()
    # first_guess_entropy = load_first_guess_entropy()

    # if (len(guess_matrix) == 0) or (len(first_guess_entropy) == 0):
    #     print('Error loading data')
        
    train = WordleTrain(guess_matrix, word_to_index, first_guess_entropy)
    train.solve()