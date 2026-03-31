import random
import string

""" 
Wordle Game

This module contains game logic for Wordle  

Aim to guess a five letter word in 6 guesses using the result that
categorises each letter in the guess

Green letter G = Letter is in the answer and also the correct position
Yellow Y = Letter is in the word but wrong position
Grey _ = Letter is not in the word

"""

WORD_LEN = 5
MAX_GUESSES = 6

class WordleGame:
    ''' 
    Wordle Game class

    Attributes:
        answer: word set as answer in the game (str)
        word_list: list of words that are available to be guessed and set as answers
        guessed_letters: dict containing which letters have been catergorised after each guess (grey, yellow, green)
        result: pattern from the current guess compared to the answer
        solved: bool indicating if the answer has bee guessed
        num_guesses: int indicating the current guess number
    '''

    def __init__(self, answer: str = None, word_list: set = None):
        self.answer = answer
        self.word_list = word_list
        self.guessed_letters = {'Grey' : set(), 'Yellow' : set(), 'Green' : set()}
        self.result = []
        self.solved = False
        self.num_guesses = 0

    def pick_random_word(self):
        ''' Picks random word from wordlist '''
        return random.choice(self.word_list)

    def game(self, guess):
        '''
        Function containing majority of the game logic
        After each guess adds the result to a dict containing all letters used

        Args:
            guess: word that has been guessed (str)
        
        Returns:
            result: string of indicating what letters are correct from the guess

        '''
        
        # Gets result from guess compared to answer
        self.result = self.pattern(guess, self.answer)

        # Update Guessed Letter Dict           
        # Meant to emulate the keyboard display
        # If a letter is green and yellow in the current guess green takes prioity
        for i in range(WORD_LEN):
            if self.result[i] == 'G':
                self.guessed_letters['Green'].add(guess[i].upper())            
            if self.result[i] == 'Y':
                self.guessed_letters['Yellow'].add(guess[i].upper())            
            if self.result[i] == '_':
                self.guessed_letters['Grey'].add(guess[i].upper())

        # Letter cannot be grey and another colour
        self.guessed_letters['Grey'] = self.guessed_letters['Grey'] - self.guessed_letters['Green'] - self.guessed_letters['Yellow']

        # Sets yellow letter to green if found
        self.guessed_letters['Yellow'] = self.guessed_letters['Yellow'] - self.guessed_letters['Green']

        return self.result

    def pattern(self, guess, answer):
        '''
        Returns a string of indicating what letters are correct from the guess
        G = Green
        Y = Yellow
        _ = Grey

        Args:
            guess: string of user's guessed/inputted word

        Return:
            result: result comparing the answer and the guess
        '''
        self.result = ["."] * WORD_LEN
        answer_letters = list(answer)

        # Check for greens
        for i in range(WORD_LEN):
            if guess[i] == answer[i]:
                self.result[i] = "G"
                # Set letter as seen
                answer_letters[i] = None

        # Check for greys and yellows
        for i in range(WORD_LEN):
            if self.result[i] == ".":
                if guess[i] in answer_letters:
                    self.result[i] = "Y"
                    # set letter as seen
                    answer_letters[answer_letters.index(guess[i])] = None
                # Set grey
                else:
                    self.result[i] = "_"

        return self.result

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
    print("Unused:", " ".join(sorted(unused)))
    
def run_game(word_list, answer):
    '''
    Main function to run game

    Args:
        word_list: list of words defined in program args
        answer: word set as answer to the game in program args
    '''

    wordle = WordleGame(answer, word_list)
 
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
        guess = input("Enter a word: ").lower()

        while not wordle.check_input(guess):
            guess = input("Enter a valid word: ")

        # Compares guess to answer
        wordle.game(guess)
        print(f'\nRESULT: {" ".join(wordle.result)}')

        print_guessed_letters(wordle.guessed_letters)

        print("-----------------------")
        wordle.solved = wordle.check(guess)
        wordle.num_guesses += 1

    # Game is Finished
    print("\n======================")
    print("    GAME FINISHED   ")
    print("======================")

    if wordle.solved:
        print(f"\nWord guessed correctly, you did it in {wordle.num_guesses} guesses")
    else:
        print("\nThe correct word was: " + wordle.answer)
    


