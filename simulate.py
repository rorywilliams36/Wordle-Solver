import numpy as np
import os
from wordle_game import *
from wordle_solver import *


WORDS = np.loadtxt('words.txt', dtype = str)
PATH = 'C:/Users/roryw/Documents/Wordle Solver'

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def get_letter_freq():
    '''
    Returns dict where each key is a letter and contains an array of occurances of that letter in that position
    '''
    freqs = dict()
    for i in alphabet:
        freqs[i] = [0, 0, 0, 0, 0]

    for w in WORDS:
        for l in alphabet:
            for i in range(0,5):
                if w[i] == l:
                    freqs[l][i] += 1

    for k in freqs:
        for i in range(0,5):
            freqs[k][i] = freqs[k][i]

    np.save(f"{PATH}/letter_freqs.npy", freqs)


def create_scores():
    '''Creates a score for words based on probability of letters occuring'''
    freqs = np.load("letter_freqs.npy", allow_pickle=True).tolist()
    
    probs = dict()
    for w in WORDS:
        probs[w] = 0
        for i in range(0, 5):
            l = w[i]
            probs[w] += freqs[l][i]
    print(probs)

    # np.save(f"{PATH}/word_scores.npy", probs)


if __name__ == "__main__":
    create_scores()
    # wordle = WordleGame()
    # solver = WordleSolver()

    # d = []
    # for w in WORDS:
    #     wordle.answer = w
    #     wordle.num_guesses = 0
    #     wordle.solved = False
    #     guess = 'irate'
        
    #     while not wordle.solved and wordle.num_guesses > 6:
    #         wordle.guessed(guess)
    #         wordle.solved = wordle.check(guess)
            
    #         solver.allocate_letters(wordle.output)

    #         solver.filter()

    #         if len(solver.green) == 0:
    #             solver.get_yellows()
    #         else:
    #             solver.get_greens()

    #         solver.get_guesses()
    #         scores = solver.get_guess_scores()

    #         guess = scores[0]
    #         wordle.num_guesses += 1
        
    #     d.append(wordle.num_guesses)

    # total = 0
    # for i in d:
    #     total += i

    # print(total/len(d))


