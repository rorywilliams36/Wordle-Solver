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
        G = Green
        Y = Yellow
        _ = Grey

        """
        self.output = ['.'] * len(guessed)

        # Game rules/logic
        if self.answer != None and guessed != None:
            for i in range(len(self.answer)):
                # Gets indexes of the letter at i in both the answer and guess
                mult_ans_l = len([j for j, l in enumerate(self.answer) if l == guessed[i]])
                # gets indexes of letter at i in the guessed word
                mult_guess_l =  len([j for j, l in enumerate(guessed) if l == guessed[i]])

                # Sets Greens
                if self.answer[i] == guessed[i]:
                    self.output[i] = 'G'
            
                elif self.output[i] != 'G':
                    # Checks for yellows
                    if self.answer.__contains__(guessed[i]):
                        # checks for double letters 
                        # if letter occurs more than once in both answer and guess set the next occurence to gray
                        if mult_ans_l >= mult_guess_l:
                            self.output[i] = 'Y'
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
        print(" G = Green Letter ")
        print(" Y = Yellow Letter ")
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
    


