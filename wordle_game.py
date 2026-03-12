import random, string
import numpy as np

WORD_LEN = 5
MAX_GUESSES = 6

class WordleGame:

    def __init__(self, answer: str = None):
        self.answer = answer
        self.word_list = np.loadtxt('data/words.txt', dtype = str)
        self.guessed_letters = {'Grey' : set(), 'Yellow' : set(), 'Green' : set()}
        self.guess = ""
        self.output = []
        self.solved = False
        self.num_guesses = 0

    def pick_random_word(self):
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
                self.guessed_letters['Green'].add(guess[i].upper())

        # Check for greys and yellows
        for i in range(WORD_LEN):
            if self.output[i] == ".":
                if guess[i] in answer_letters:
                    self.output[i] = "Y"
                    # set letter as seen
                    answer_letters[answer_letters.index(guess[i])] = None
                    self.guessed_letters['Yellow'].add(guess[i].upper())
                # Set grey
                else:
                    self.output[i] = "_"
                    self.guessed_letters['Grey'].add(guess[i].upper())
                    

        # Letter cannot be grey and another colour
        self.guessed_letters['Grey'] = self.guessed_letters['Grey'] - self.guessed_letters['Green'] - self.guessed_letters['Yellow']

        return self.output

    def check(self, guess):
        ''' Win condition '''
        if guess == self.answer:
            return True
        return False

    def check_input(self, guess):
        ''' 
        Validates user's guessed/inputted word

        Args:
            guess: string of user's input

        Return:
            boolean stating whether guess is valid
        '''

        if len(guess) != WORD_LEN and (guess not in self.word_list):
            return False
        if not guess.isalpha():
            return False
        return True

def print_guessed_letters(guessed_letters):
    ''' Prints all letters used in guesses and all remaining '''
    greys = guessed_letters['Grey']
    yellows = guessed_letters['Yellow']
    greens = guessed_letters['Green']
    unused = set(string.ascii_uppercase) - greens - yellows - greys

    print("\nLETTERS USED/REMAINING:")
    print("Green :", " ".join(sorted(greens)))
    print("Yellow:", " ".join(sorted(yellows)))
    print("Grey  :", " ".join(sorted(greys)))
    print("Remaining:", " ".join(sorted(unused)))
    
def run_game(answer):
    wordle = WordleGame(answer)
 
    # Sets random word as answer if no word is set
    if wordle.answer is None:
        wordle.answer = wordle.pick_random_word()
    
    # Game UI/Rules
    print("-------- Wordle --------")
    print(" G = Green Letter ")
    print(" Y = Yellow Letter ")
    print(" _ = Grey Letter\n")
    print("Must enter a 5 letter word")
    print("Press crtl+c to exit")

    # user input for guess
    while not wordle.solved and wordle.num_guesses < MAX_GUESSES:
        print(f"\nGuesses left: {MAX_GUESSES - wordle.num_guesses}")
        wordle.guess = input("Enter a word: ").lower()

        while not wordle.check_input(wordle.guess):
            wordle.guess = input("Enter a valid word: ")

        # Compares guess to answer
        wordle.game(wordle.guess)
        print(f'\nRESULT: {" ".join(wordle.output)}')

        print_guessed_letters(wordle.guessed_letters)

        print("-----------------------")
        wordle.solved = wordle.check(wordle.guess)
        wordle.num_guesses += 1

    # Game is Finished
    print("\n======================")
    print("    GAME FINISHED   ")
    print("======================")

    if wordle.solved:
        print(f"\nWord guessed correctly, you did it in {wordle.num_guesses} guesses")
    else:
        print("\nThe correct word was: " + wordle.answer)
    


