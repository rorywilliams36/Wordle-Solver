import os
import sys
import json
import numpy as np

from solver.data_utils import load_json, load_word_to_index

GUESS_SCORE_FILE = 'guess_scores'
GUESS_RECORD_FILE = 'guess_record' 

def load_guess_scores(word_list):
    ''' Loads the guess_score file and converts the guess indexes into the guess string'''
    guess_scores_json = load_json(GUESS_SCORE_FILE)
    word_to_index = load_word_to_index(word_list)
    guess_score_dict = {}

    words = guess_scores_json.keys()

    for w in words:
        guess_score_dict[w] = []
        turns = len(guess_scores_json[w])
        for t in range(turns):
            turns_pos_guesses = guess_scores_json[w][t]
            for guess in turns_pos_guesses:
                guess[0] = list(word_to_index.keys())[guess[0]]

            guess_score_dict[w].append(turns_pos_guesses)

    return guess_score_dict


# Print Functions
def print_result_index(word_list, answer):
    ''' Prints results form the guess record and scores given the answer word string'''
    guess_scores = load_guess_scores(word_list)
    guess_record = load_json(GUESS_RECORD_FILE)

    if (answer in guess_scores) and (answer in guess_record):
        record = guess_record[answer]
        scores = guess_scores[answer]
        print(record)

        print('\n====================')
        print('Guess Record: ')
        print(f'Answer: {answer}')
        turns = len(record)
        for turn in range(turns):
            print(f'{turn+1}: Guess: {record[turn]['Guess']}, Result: {record[turn]['Result']}')

        print('\n====================')
        print('Guess Scores: ')
        print(f'Columns: Guess, Entropy, Entropy Ratio, Worst Case Ratio, Word Prob, Score')
        print(f'Answer: {answer}')
        for t in range(turns):
            print(f'\nGuess {t+1}:')
            guess = scores[t]
            for g in guess:
                print(g)

    else:
        print(f'\'{answer}\' is not found in the results')


def print_guess_scores(word_list):
    ''' Print guess_scores.json file'''
    guess_scores = load_guess_scores(word_list)
    words = guess_scores.keys()
    print(f'Columns: Guess, Entropy, Entropy Ratio, Worst Case Ratio, Word Prob, Score')

    for w in words:
        print('\n===========')
        print(f'Answer: {w}')
        game = guess_scores[w]
        turns = len(game)
        for t in range(turns):
            rank = 1
            print(f'\nGuess {t+1}:')
            guess = guess_scores[w][t]
            for g in guess:
                print(f'{rank}. {g}')
                rank += 1
    

def print_guess_record():
    ''' Prints guess_record.json file '''
    guess_record = load_json(GUESS_RECORD_FILE)
    answers = list(guess_record.keys())[:-2]
    for w in answers:
        print('\n===========')
        print(f'Answer: {w}')
        game = guess_record[w]
        turns = len(game)
        for turn in range(turns):
            print(f'{turn+1}: {game[turn]['Guess']} {game[turn]['Result']}')


    guess_distribution = guess_record['Distribution']
    unsolved = sum(guess_distribution[6:])

    print('\n==================================')
    print(f'Guess Distribution: {guess_distribution}')
    print(f'Average Guesses: {guess_record['Average_Guesses']}')
    print(f'Words found in 6< guesses: {unsolved}')
    print(f'Words unsolved/not found: {guess_distribution[-1]}')
