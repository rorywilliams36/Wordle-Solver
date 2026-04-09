"""
Data Utils

This module contains functions in the writing and loading files in the /data folder and also
any functions to be used before running the solver for the first time

"""

import os
import sys
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from wordle_game import WordleGame

PATH = f'{os.path.abspath(os.getcwd())}/data'

def create_guess_matrix(word_list):
    '''
    Creates matrix where matrix[guess][answer] is the comparison of words using 
    wordle game logic

    Matrix saves time since the comparisons between guesses and answers never change
    '''

    print('Building Guess Matrix')
    
    # Initalise matrix
    word_list_len = len(word_list)
    guess_matrix = np.empty((word_list_len, word_list_len), dtype=np.dtype('U100'))
    wordle = WordleGame()

    word_list = list(word_list)

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
        print(f"Error creating guess matrix: \n{e}")

def find_first_guess(word_list, word_to_index, guess_matrix):
    '''
    Calculates the expected information gained (entropy) for every word as a first guess 
    
    Args:
        word_list: set of words
        word_to_index: dict containing word index pairs to be used for lookups in guess matrix
        guess_matrix: array containing all possible results for a given guess and answer combination
    '''

    # import entropy calc from other module
    from solver.train import entropy

    guess_entropy = {}
    
    print('Calculating Entropies')

    for guess in word_list:
        pattern_counts = {}
        for answer in word_list:
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
        H = entropy(pattern_counts)
        guess_entropy[guess] = H

    entropy_file_path = f"{PATH}/first_guess_entropy.json"

    # Save values as JSON
    try:
        with open(entropy_file_path, 'w') as f:
            json.dump(guess_entropy, f)
    except Exception as e:
        print(f'Error saving entropy file: \n{e}')

def apply_sigmoid():
    ''' Applies sigmoid function to wordlist to calculate a probability for word being the answer '''

    print('Calculating Word Probabilites')

    most_likely = load_wordlist()


    # Apply sigmoid function (z)

    # Attach sigmoid value to words
    word_prob = {}

    N = len(most_likely) # number of values
    alpha = 15 # how fast values drop
    beta = 0.35 # sets midpoint of curve (35% word is 0.5)
    for rank, word in enumerate(most_likely):
        word = most_likely[rank].strip()

        x = (rank) / (N - 1)
        z = 1/(1 + np.exp(alpha*(x - beta)))
        word_prob[word] = z

    # Save values
    word_prob_path = f"{PATH}/word_probabilites.json"
    try:
        with open(word_prob_path, 'w') as f:
            json.dump(word_prob, f)
    except Exception as e:
        print(f'Error saving word probabilities: \n{e}')

# Load Data
def load_guess_matrix(word_list):
    '''
    Loads the guess matrix containing all results for each guess and answer
    Creates an indexing tool so that the guess matrix can be correctly accessed

    Args:
        word_list

    Returns
        word_to_index: dict containing the index of each word in the guess matrix
        guess_matrix: array containing all possible results given the indices of the guess and answer
    '''
    # Load guess lookup matrix
    guess_matrix = []
    word_to_index = {}
    try:
        guess_matrix = np.load(f"{PATH}/guess_matrix.npy", allow_pickle=True)
        word_to_index = load_word_to_index(word_list) # Indexing table for each word
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error loading guess matrix: \n{e}')
    return guess_matrix, word_to_index

def load_word_to_index(word_list):
    ''' Creates indexing tool to be used with the guess matrix'''
    return {w:i for i,w in enumerate(word_list)}

def save_json(f_name, data):
    ''' Loads the JSON file given by filename (f_name) '''
    try:
        with open(f"{PATH}/{f_name}.json", "w") as f:
            json_file = json.dump(data, f)
            f.close()
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error writing JSON file: \n{e}')


def load_json(f_name):
    ''' Loads the JSON file given by filename (f_name) '''
    json_file = {}
    try:
        with open(f"{PATH}/{f_name}.json", "r") as f:
            json_file = json.load(f)
            f.close()
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error loading JSON file: \n{e}')
    return json_file

def load_wordlist():
    ''' Loads word list '''
    most_likely = []
    try:
        with open(f"{PATH}/wordlists/words.txt", "r") as f:
            most_likely = f.readlines()
            f.close()
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error loading word list: \n{e}')
    return most_likely