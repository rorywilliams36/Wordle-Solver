import numpy as np
import random

class WordleGame:

    def __init__(self, answer: str = None, sim: bool = False):
        self.answer = 'eerie'
        self.word_list = np.loadtxt('words.txt', dtype = str)
        self.guesses = np.array([])
        self.guessed = ""
        self.output = []
        self.sim = sim
        self.solved = False
        self.num_guesses = 0

    def pickRandomWord(self):
        return random.choice(self.word_list)

    def guess(self, guessed):
        """
        Returns a string of indicating what letters are correct from the guess
        ! = Green
        % = Yellow
        _ = Grey

        """
        self.output = ['.'] * len(guessed)

        if self.answer != None and guessed != None:
            # Checks for greens
            for i in range(len(self.answer)):
                # Gets indexes of double letters in the answer and guess
                mult_letters = [j for j, l in enumerate(self.answer) if l == guessed[i]]
                mult_guess_l =  [j for j, l in enumerate(guessed) if l == guessed[i]]

                if self.answer[i] == guessed[i]:
                    self.output[i] = '!'
            
                elif self.output[i] != '!':
                    # Checks for yellows
                    if self.answer.__contains__(guessed[i]):
                        # checks for double letters 
                        # if letter occurs more than once in both answer and guess set the next occurence to gray
                        if len(mult_letters) >= len(mult_guess_l):
                            self.output[i] = '%'
                        # if the guess has mult letters and answer doesnt set the next occurances to gray
                        else:
                            self.output[i] = '_'
                            
                    else:
                        # If letter not in word then grey
                        self.output[i] = '_'
                        
        return self.output

    # Checks for win
    def check(self, guessed):
        if guessed == self.answer:
            return True
        return False

# Validates input
def checkInput(guessed):
    if len(guessed) != 5 and (guessed not in wordle.word_list):
        return False
    # checks if the input only contains letters
    if not guessed.isalpha():
        return False
    
    return True


if __name__ == "__main__":
    wordle = WordleGame()
    if not wordle.sim:
        if wordle.answer == None:
            wordle.answer = wordle.pickRandomWord()
        
        print("Wordle\n")
        print(" ! = Green Letter ")
        print(" % = Yellow Letter ")
        print(" _ = Grey Letter\n")
        print("Must enter a a 5 letter word")
        print("Press crtl+c to exit\n")

        while not wordle.solved and wordle.num_guesses < 6:
            print(f"\nGuesses left: {6 - wordle.num_guesses}")
            wordle.guessed = input("Enter a word: ").lower()

            while not checkInput(wordle.guessed):
                wordle.guessed = input("Enter a valid word: ")

            wordle.guess(wordle.guessed)
            print("".join(wordle.output))
            wordle.solved = wordle.check(wordle.guessed)
            wordle.num_guesses += 1

        if wordle.solved:
            print(f"\nWord guess correctly, you did it in {wordle.num_guesses} guesses")
        else:
            print("\nThe correct word was: " + wordle.answer)
    


