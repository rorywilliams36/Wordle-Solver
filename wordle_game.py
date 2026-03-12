import numpy as np
import random

WORD_LEN = 5

class WordleGame:

    def __init__(self, answer: str = None, sim: bool = False):
        self.answer = 'abide'
        self.word_list = np.loadtxt('words.txt', dtype = str)
        self.guesses = np.array([])
        self.guess = ""
        self.output = []
        self.sim = sim
        self.solved = False
        self.num_guesses = 0

    def pickRandomWord(self):
        ''' Picks random word from wordlist '''
        return random.choice(self.word_list)

    def game(self, guess):
        """
        Returns a string of indicating what letters are correct from the guess
        G = Green
        Y = Yellow
        _ = Grey

        Args:
            guess: string of user's guessed/inputted word

        Return:
            output: result comparing the answer and the guess
        """
        
        self.output = ["."] * WORD_LEN
        answer_letters = list(self.answer)

        # Check for greens
        for i in range(WORD_LEN):
            if guess[i] == self.answer[i]:
                self.output[i] = "G"
                # Set letter as seen
                answer_letters[i] = None

        # Check for greys and yellows
        for i in range(WORD_LEN):
            if self.output[i] == ".":
                if guess[i] in answer_letters:
                    self.output[i] = "Y"
                    # set letter as seen
                    answer_letters[answer_letters.index(guess[i])] = None
                # Set grey
                else:
                    self.output[i] = "_"
                        
        return self.output

    def check(self, guess):
        ''' Win condition '''
        if guess == self.answer:
            return True
        return False

def checkInput(guess):
    ''' 
    Validates user's guessed/inputted word

    Args:
        guess: string of user's input

    Return:
        boolean stating whether guess is valid
    '''

    if len(guess) != WORD_LEN and (guess not in wordle.word_list):
        return False
    if not guess.isalpha():
        return False
    return True

if __name__ == "__main__":
    wordle = WordleGame()
    if not wordle.sim:
        # Sets random word as answer if no word is set
        if wordle.answer == None:
            wordle.answer = wordle.pickRandomWord()
        
        # Game UI/Rules
        print("Wordle\n")
        print(" G = Green Letter ")
        print(" Y = Yellow Letter ")
        print(" _ = Grey Letter\n")
        print("Must enter a a 5 letter word")
        print("Press crtl+c to exit\n")

        # user input for guess
        while not wordle.solved and wordle.num_guesses < 6:
            print(f"\nGuesses left: {6 - wordle.num_guesses}")
            wordle.guess = input("Enter a word: ").lower()

            while not checkInput(wordle.guess):
                wordle.guess = input("Enter a valid word: ")

            # Compares guess to answer
            wordle.game(wordle.guess)
            print("".join(wordle.output))
            wordle.solved = wordle.check(wordle.guess)
            wordle.num_guesses += 1

        # Game is Finished
        if wordle.solved:
            print(f"\nWord guess correctly, you did it in {wordle.num_guesses} guesses")
        else:
            print("\nThe correct word was: " + wordle.answer)
    


