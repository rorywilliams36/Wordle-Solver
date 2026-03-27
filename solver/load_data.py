import os
import sys
import json
import numpy as np

PATH = f'{os.path.abspath(os.getcwd())}/data'

# Load Data
def load_guess_matrix(word_list):
    '''
    Loads the guess matrix containing all results for each guess and answer
    Creates an indexing tool so that the guess matrix can be correctly accessed
    '''
    # Load guess lookup matrix
    guess_matrix = []
    word_to_index = {}
    try:
        guess_matrix = np.load(f"{PATH}/guess_matrix.npy", allow_pickle=True)
        word_to_index = {w:i for i,w in enumerate(word_list)} # Indexing table for each word
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error: {e}')
    return guess_matrix, word_to_index

def load_first_guess_entropy():
    '''
    Loads the JSON file containing entropy values for the first guess
    '''
    first_guesses = {}
    try:
        with open(f"{PATH}/first_guess_entropy.json", "r") as f:
            first_guesses = json.load(f)
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error: {e}')
    return first_guesses

def load_word_probs():
    ''' Loads the file word_probs'''
    word_probs = {}
    try:
        with open(f"{PATH}/word_probabilites.json", "r") as f:
            word_probs = json.load(f)
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print(f'Error: {e}')
    return word_probs