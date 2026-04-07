import os
import random
import sys
import numpy as np

from solver.filters import WordleFilter
import solver.data_utils as d_utils

"""
solve

This module contains code used to solve and give recommnedation guesses for Wordle

"""


MAX_GUESSES = 6

# File path and Names
PATH = f'{os.path.abspath(os.getcwd())}/data'
GUESS_ENTROPYS = 'first_guess_entropy'
WORD_PROBS = 'word_probabilites'


class WordleSolver:
    '''
    Wordle Solver Class:
    Contains relevant functions to be used to help solve the Wordle game

    Attributes: 
        guess_matrix: array containing all possible results for a given guess and answer combination
        word_to_index: dict that contains a given words index in the guess matrix
        first_guess_entropy: contains all word's entropy values when the word is used as the first guess
        word_probs: dict containing the probability that the word is likely to be the answer
        word_list: array of words available to be used as guesses and answers
    '''
    
    def __init__(self, guess_matrix, word_to_index, first_guess_entropy, word_probs, word_list, 
                    weights: tuple = (1,1,1)):
        self.guess_matrix = guess_matrix
        self.word_to_index = word_to_index
        self.first_guess_entropy = first_guess_entropy
        self.word_probs = word_probs
        self.word_list = word_list
        self.weights = weights

    def simulate_games(self, random_samples, first_guess: str = None):
        '''
        Plays every possible Wordle game using a set word as the first guess

        Args:
            first_guess: str word to be set as the inital guess

        Returns:
            avg number of guesses for the game
        '''

        N = len(self.word_list)
        first_guess = None


        # Set first guess if none is defined
        first_entropy = 0
        if (first_guess is None) or (not self.first_guess_entropy.get(first_guess)):
            first_guess = max(self.first_guess_entropy, key = self.first_guess_entropy.get)
            first_entropy = self.first_guess_entropy[first_guess]

        num_guesses = []
        guess_record = {}
        total_guess_stats = {}
        guess_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # last idx is 10+/unsolved

        # Get values for first guess to record
        max_first_guess_entropy = -np.log2(1/N)
        first_entropy_ratio = max_first_guess_entropy / first_entropy
        first_word_prob = self.get_word_probabilities(self.word_list, first_guess)
        first_score = self.expected_score(first_entropy, first_word_prob, max_first_guess_entropy, 0)

        if random_samples > 0:
            words = random.sample(self.word_list, random_samples)
        else:
            words = list(self.word_list)

        for i, answer in enumerate(words):
            filters = WordleFilter(self.word_list)

            guess = first_guess
            entropy = first_entropy
            pos_answers_remain = N
            guess_num = 0
            solved = False
            print('================')
            print(f'{i} Answer: {answer}')

            # Set containing all submitted guesses
            # avoids same guess being submitted if contains the same letters
            # as answer but in different order
            completed_guesses = set()
            guess_record[answer] = []
            total_guess_stats[answer] = []
            total_guess_stats[answer].append([(self.word_to_index[first_guess], first_entropy, first_entropy_ratio, 0, first_word_prob, first_score)])

            while (not solved):
                guess_num += 1

                max_entropy = -np.log2(1/pos_answers_remain)      

                # gets result for chosen guess
                res = self.get_result(guess, answer)

                # add guess to record
                # print(f'{guess_num, guess, res, entropy, pos_answers_remain}') # pos_answers_remain = num possible answers before guess is made
                guess_record[answer].append(({'Num': guess_num, 'Guess': guess, 'Result': res}))

                # Set guess as submitted 
                completed_guesses.add(guess)
                if guess == answer:
                    solved = True
                    break
                
                # Filtering
                # Update and get all grey, yellow and green letter sets from result 
                filters.grey, filters.yellow, filters.green = filters.allocate_letters(guess, res)

                # get and update letter counts from result
                curr_max_counts, curr_min_counts = filters.create_count_contraint(guess, res)
                filters.max_counts, filters.min_counts = filters.update_count_contraints(curr_min_counts, curr_max_counts)

                #  New filtered wordlists
                pos_answers, allowed_guesses = filters.filter()

                # remove already submitted guesses from wordlist
                pos_answers = pos_answers - completed_guesses
                allowed_guesses = allowed_guesses - completed_guesses

                # checks if there are any guesses to be made
                # Gets the word to be guesses next
                if len(pos_answers) > 0:
                    pos_guess_scores, guess_stats = self.get_possible_guess_scores(pos_answers, allowed_guesses, max_entropy)
                    guess = max(pos_guess_scores, key = pos_guess_scores.get)
                    entropy = pos_guess_scores[guess]
                    pos_answers_remain = len(pos_answers)
                    total_guess_stats[answer].append(guess_stats)

                    
                # if no guesses available set to unsolved
                else:
                    guess_num = len(guess_distribution)-1
                    break
         
            # record guess number
            num_guesses.append(guess_num)
            if guess_num <= 9:
                guess_distribution[guess_num-1] += 1
            else:
                solved = True
                guess_distribution[-1] += 1

            # if guess_num > 6:
            #     print(f'\n{answer}')
            #     print(guess_record[answer])
            #     print('========================')


            progress_bar(i, len(words))
        unsolved = sum(guess_distribution[6:])
        avg_guess = np.mean(num_guesses)

        print('\n==================================')
        print(f'Guess Distribution: {guess_distribution}')
        print(f'Mean Guesses to solve: {avg_guess}')
        print(f'Words found in 6< guesses: {unsolved}')
        print(f'Words unsolved/not found: {guess_distribution[-1]}')
        return avg_guess, guess_distribution, guess_record, total_guess_stats

    def get_possible_guess_scores(self, pos_answers, allowed_guesses, max_entropy):
        ''' 
        Calculates expected score for all possible guesses left

        Args:
            pos_answers: set of words that are possible answers
            allowed_guesses: set of words that dont contain grey letters (contains words not possible to be answers)
            max_entropy: float for the maximum value the entropy for a word can be

        Returns:
            pos_guess_scores: dict containing entropy values for the possible guesses
        '''
        pos_guess_scores = {}
        pos_guess_stats = []
        pos_answers_len = len(pos_answers)

        for guess in allowed_guesses:
            pattern_counts = {}

            for answer in pos_answers:
                # Lookup result for guess and answer
                res = self.get_result(guess, answer)

                # Increment result occurence
                pattern_counts[res] = pattern_counts.get(res, 0) + 1

            # Calculate entropy for word
            H = entropy(pattern_counts)
            word_prob = self.get_word_probabilities(pos_answers, guess)
            worst_case_ratio = self.get_worst_case(pattern_counts)

            # get score
            score = self.expected_score(H, word_prob, max_entropy, worst_case_ratio)

            # print(guess, H, score, max_entropy, word_prob)
            pos_guess_scores[guess] = score
            pos_guess_stats.append((self.word_to_index[guess], H, H/max_entropy, worst_case_ratio, word_prob, score))

        sorted_guess_stats = sorted(pos_guess_stats, key=lambda x: x[-1], reverse=True)[:10]
    
        return pos_guess_scores, sorted_guess_stats

    def get_result(self, guess, answer):
        ''' Lookup result from guess matrix given the guess and answer '''
        g_idx = self.word_to_index[guess]
        a_idx = self.word_to_index[answer]
        res = self.guess_matrix[g_idx][a_idx]
        return res

# Score Calculations
    def get_word_probabilities(self, pos_answers, guess):
        '''
        Gets probability value for the relevant word from preset values
        Probability value is based on how common the word is

        Args:
            pos_answers: set of all possible answers
            guess: word currently used as guess

        Return:
            word_prob: float of the probability the word is likely answer
        '''

        worst_word_prob = self.word_probs['pupal'] * 0.1

        # Get word probability
        # if guess is not a possible answer
        if guess not in pos_answers:
            word_prob = 0
        # if guess is an uncommon word set probability to unlikely
        elif not self.word_probs.get(guess):
            word_prob = worst_word_prob
        else:
            word_prob = self.word_probs[guess]
        return word_prob

    def get_worst_case(self, pattern_counts):
        '''
        Calculates the worst case ratio 
    
        Args:
            pattern_count: dict containing all possible results and their occurences

        Returns
            worst_case_ratio (float): Worst case of answers left to total number of possible answers
        '''
        worst_case = max(pattern_counts.values())
        worst_case_ratio = 1 - (worst_case / sum(pattern_counts.values()))
        return worst_case_ratio

    def expected_score(self, H, word_prob, max_entropy, worst_case_ratio):
        ''' 
        Calculates the expected score of a word
        Combines the entropy ratio, word proability and worst case of possible answers left into a single metric

        Args:
            H: entropy value for that guess
            word_prob: probability the guess is likely the answer (defined using sigmoid function)
            max_entropy: the maximum value entropy can be for that guess (also known as uncertainty)
            word_left: ratio between the worst case of possible answerx left after the guess and number of possible answers currently

        Returns:
            (float) word score using weighted sum
        '''
        w1, w2, w3 = self.weights
        entropy_ratio = H / max_entropy
        return w1*entropy_ratio +  w2*word_prob + w3*worst_case_ratio


def entropy(pattern_counts):
    '''
    Finds expected value (information entropy) for guess
    i.e Average information gained for a particular guess
    H = - (Sumof [(p(x)) * log2(p(x))])

    Args:
        pattern_counts: dict containing counters for occurences of each result/pattern

    Returns:
        H: Entropy value (float)
    '''
    H = 0
    counts = pattern_counts.values()
    total = sum(counts)
    for count in counts:
        p = count / total
        if p > 0:
            H -= p * np.log2(p)
      
    return H



# Main Functions
def run_gather_data(word_list):
    ''' 
    Runs functions used to create/calculate the data needed to run solver

    Args:
        word_list: list/set of words defined in program args
    '''
    solver = WordleSolver(None, {}, {}, {}, word_list)
    d_utils.create_guess_matrix(word_list)
    guess_matrix, word_to_index = d_utils.load_guess_matrix(word_list)
    d_utils.find_first_guess(word_list, word_to_index, guess_matrix)
    d_utils.apply_sigmoid()

def run_solver(word_list, first_guess, test: bool = True, train_iter: int = 10, random_samples: int = 0):
    ''' 
    Runs simulation of every possible wordle game
    
    Args:
        word_list: list/set of words defined in main program args
        first_guess: word set to be the first guess in all games defined in main program args 
        train_iter: int to set the number of iterations to be used when training
        random_samples: int of the number of random samples used for the solver
    '''
    # Load data
    guess_matrix, word_to_index = d_utils.load_guess_matrix(word_list)
    first_guess_entropy = d_utils.load_json(GUESS_ENTROPYS)
    word_probs = d_utils.load_json(WORD_PROBS)

    # Check all data is loaded
    if (len(guess_matrix) == 0) or (len(first_guess_entropy) == 0) or (len(word_probs) == 0):
        print('Error loading data')
        sys.exit()
    
    # Training
    if not test:
        best_score = 4
        best_weights = (0,0,0)
        best_distribution = []

        for i in range(train_iter):
            w1 = random.uniform(0.65, 0.75) # Entropy weight (more value when selecting word) 
            w2 = random.uniform(0.1, 0.25) # Worst case weight (slight bias to word removal)
            w3 = random.uniform(0.1, 0.15) # word probability (little bias as only important when few words remain)

            print(f'\nIteration {i}/{train_iter}starting:')
            print(f'Entropy Weight: {w1}, Worst Case Weight: {w2}, Probability Weight: {w3}')

            solver = WordleSolver(guess_matrix, word_to_index, first_guess_entropy, word_probs, word_list, weights=(w1, w2, w3))
            avg_guess, guess_distribution, guess_record, guess_stats = solver.simulate_games(random_samples, first_guess)

            # Save weights if better average score
            if avg_guess < best_score:
                best_score = avg_guess
                best_distribution = guess_distribution
                best_weights = (w1, w2, w3)
                print(f'New best: {best_score}, {best_weights}')
        
        print('\n==================================')
        print(f'Best Score: {best_score}')
        print(f'Guess Distribution: {best_distribution}')
        print(f'Weights: {best_weights}')


    # Testing
    else:
        weights = (0.7254558452927472, 0.1029681643013621, 0.12866232366981367) # 3.3.56994369857081 0 3
        solver = WordleSolver(guess_matrix, word_to_index, first_guess_entropy, word_probs, word_list, weights)
        avg_guess, guess_distribution, guess_record, guess_stats = solver.simulate_games(random_samples, first_guess)
        guess_record['Average_Guesses'] = avg_guess
        guess_record['Distribution'] = guess_distribution

        d_utils.save_json('guess_record', guess_record)
        d_utils.save_json('guess_scores', guess_stats)

# misc
def progress_bar(current, total, bar_length=30):
    '''Progress bar'''
    percent = current / total
    filled_length = int(bar_length * percent)
    p_bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{p_bar}] {current}/{total-1} words')
    sys.stdout.flush()
