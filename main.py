import argparse
import numpy as np

from wordle_game import run_game
from solver.solve import run_gather_data, run_solver
from solver.data_utils import load_json, print_guess_scores

"""
Main module to run the Wordle game or solver using the relevant arguments
"""

GUESS_LIST = sorted(set(np.loadtxt("data/wordlists/guess_wordlist.txt", dtype=str)))
ANSWER_LIST = sorted(set(np.loadtxt("data/wordlists/answer_wordlist.txt", dtype=str)))
WORD_LIST = sorted(set(np.loadtxt("data/wordlists/most_common.txt", dtype=str)))

def get_wordlist(word_list_arg):
    ''' Returns wordlist given its arg '''
    if word_list_arg == 'guesses':
        return GUESS_LIST
    if word_list_arg == 'answers':
        return ANSWER_LIST
    return WORD_LIST

def validate_word_inputs(word_list, input_word):
    ''' Checks if word defined in arg is valid (word set for first guess, etc) '''
    if input_word is not None:
        if (input_word in word_list) or ((len(input_word) == 5) and (input_word.isalpha())):
            return input_word
        print(f'{input_word}: is not valid to use. The first guess will be the word with largest entropy')
    return None

def validate_answer(word_list, input_word):
    ''' Checks if word set as answer is contained in the defined word list '''
    if input_word is not None:
        if input_word in word_list:
            return input_word
        print(f'{input_word}: is not valid to use. The answer will be randomised from the word list')
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Wordle Game and Solver")

    # Run code
    parser.add_argument('-g', '--game', action='store_true', help="Run Wordle Game")
    parser.add_argument('-s', '--solver', action='store_true', help="Run Wordle Solver")
    parser.add_argument('-ts', '--train_solver', action='store_true', help="Trains the solver to find best weights used in word scoring")
    parser.add_argument('-gd', '--gather_data', action='store_true', help="Creates guess matrix, calculates first guess entropies and word probabilites (must be ran before using solver (testing and training))")
    parser.add_argument('-r', '--results', action='store_true', help="View Results for the previous solver run")

    # Set Variables
    parser.add_argument('-sa', '--set_answer', type=str, help="Set Wordle Answer (Only used when playing the game)", default=None)
    parser.add_argument('-wl', '--set_wordlist', type=str, choices=['answers', 'guesses', 'most_common'], help="Set wordlist using either (all previous answer in Wordle, all allowed guesses in Wordle, most common 5 letter words)", default='most_common')
    parser.add_argument('-fg', '--set_first_guess', type=str, help='Sets first guess used in solver', default=None)
    parser.add_argument('-ti', '--set_train_iterations', type=int, help='Sets the number of iterations used in training', default=10)
    parser.add_argument('-rs', '--random_samples', type=int , help='Sets the number random samples of words when using the solver (if not set use the entire wordlist)', default=0)

    # Get Args
    args = parser.parse_args()

    # Validate args
    word_list = get_wordlist(args.set_wordlist)
    answer = validate_answer(word_list, args.set_answer)
    first_guess = validate_word_inputs(word_list, args.set_first_guess)

    if args.game:
        run_game(word_list, answer)

    if args.gather_data:
        run_gather_data(word_list)

    if args.solver or args.train_solver:
        test = False if args.train_solver is None else True
        run_solver(word_list, first_guess, test, args.set_train_iterations, args.random_samples)

    if args.results:
        print_guess_scores(word_list)