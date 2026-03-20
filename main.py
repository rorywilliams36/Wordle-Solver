import argparse
import numpy as np

from wordle_game import run_game
from solver.train import run_gather_data, run_solver

GUESS_LIST = sorted(set(np.loadtxt("data/wordlists/guess_wordlist.txt", dtype=str)))
ANSWER_LIST = sorted(set(np.loadtxt("data/wordlists/answer_wordlist.txt", dtype=str)))
WORD_LIST = sorted(set(np.loadtxt("data/wordlists/words.txt", dtype=str)))


def get_wordlist(word_list_arg):
    if word_list_arg == 'guesses':
        return GUESS_LIST
    if word_list_arg == 'answers':
        return ANSWER_LIST
    return WORD_LIST

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Wordle Game and Solver")

    # Run code
    parser.add_argument('-g', '--game', action='store_true', help="Run Wordle Game")
    parser.add_argument('-s', '--solver', action='store_true', help="Run Wordle Solver")
    parser.add_argument('-gd', '--gather_data', action='store_true', help="Creates guess matrix and calculate entropies for first guesses (Must be ran before using solver)")
    parser.add_argument('-gs', '--game_solver', action='store_true', help="Run Game and Solver")

    # Set Variables
    parser.add_argument('--set_answer', type=str, help="Set Wordle Answer", default=None)
    parser.add_argument('--set_wordlist', type=str, choices=['answers', 'guesses', 'most_common'], help="Set wordlist", default='most_common')
    parser.add_argument('--set_first_guess', type=str, help='Sets first guess used in solver', default=None)
    
    # Get Args
    args = parser.parse_args()
    answer = args.set_answer
    word_list = get_wordlist(args.set_wordlist)
    
    if args.game:
        run_game(word_list, args.set_answer)

    if args.gather_data:
        run_gather_data(word_list)

    if args.solver:
        run_solver(word_list, args.set_first_guess)

