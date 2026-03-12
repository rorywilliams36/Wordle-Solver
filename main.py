import argparse

from wordle_game import run_game

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Wordle Game and Solver")
    parser.add_argument('--game', action='store_true', default=True, help="Run Wordle Game")
    parser.add_argument('--solver', action='store_true', default=False, help="Run Wordle Solver")
    parser.add_argument('-gs', action='store_true', help="Run Game and Solver")
    parser.add_argument('--set_answer', type=str, default=None, help="Set Wordle Answer")

    args = parser.parse_args()
    if args.game:
        run_game(None)


