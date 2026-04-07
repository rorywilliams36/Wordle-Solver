import os
import sys
import json
import numpy as np

from solver.data_utils import load_json, load_word_to_index

def print_guess_scores(wordlist):
    ''' Print guess_scores.json file'''
    guess_scores = load_json('guess_scores')
    word_to_index = load_word_to_index(wordlist)
    words = guess_scores.keys()
    guess_score_dict = {}
    for w in words:
        print('===========')
        print(f'Answer: {w}')
        game = guess_scores[w]
        turns = len(game)
        for t in range(turns):
            print(f'\nNo. Guess: {t+1}')
            guess = guess_scores[w][t]
            guess_score_dict[w][t] = guess
            for g in guess:
                guessed_word_idx = g[0]
                guessed_word = list(word_to_index.keys())[guessed_word_idx]
                print(guessed_word, g[1:])
    

def print_guess_record():
    ''' Prints guess_record.json file '''
    guess_record = load_json('guess_record')
    answers = list(guess_record.keys())[:-2]
    for w in answers:
        print('\n===========')
        print(f'Answer: {w}')
        game = guess_record[w]
        turns = len(game)
        for turn in range(turns):
            print(f'{turn+1}: Guess: {game[turn]['Guess']}, Result: {game[turn]['Result']}')