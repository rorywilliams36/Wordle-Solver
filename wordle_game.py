import numpy as np
import random

class WordleGame:

    def __init__(self, answer: str = None, sim: bool = False):
        self.answer = answer
        self.word_list = np.loadtxt('words.txt', dtype = str)
        self.guesses = np.array([])
        self.sim = sim
        self.solved = False
        self.num_guesses = 0

    def pickRandomWord(self):
        return random.choice(self.word_list)

    def guess(self, guessed):
        """
        Returns a string of indicating what letters are correct from the guess
        * = Green
        % = Yellow
        _ = Grey

        Arrays are also returned for simulations
        """
        output = ['.'] * len(guessed)
        green = np.array([])
        yellow = np.array([])
        grey = np.array([])

        if self.answer != None and guessed != None:
            # Checks for greens
            for i in range(len(self.answer)):
                if self.answer[i] == guessed[i]:
                    output[i] = '*'
                    np.append(green, (guessed[i], i))
            
            for i in range(len(self.answer)):
                if output[i] != '*':
                    # Checks for yellows
                    if self.answer.__contains__(guessed[i]):
                        output[i] = '%'
                        np.append(yellow, (guessed[i], i))
                    else:
                        # If letter not in word then grey
                        output[i] = '_'
                        np.append(grey, guessed[i])

        return output, grey, yellow, green

    def check(self, guessed):
        if guessed == self.answer:
            return True
        return False


def checkInput(guessed):
    if len(guessed) != 5:
        return False
    if not guessed.isalpha():
        return False
    
    return True


if __name__ == "__main__":
    wordle = WordleGame()
    if wordle.answer == None:
        wordle.answer = wordle.pickRandomWord()

    while not wordle.solved and wordle.num_guesses < 6:
        guessed = input("\nEnter a word: ").lower()

        while not checkInput(guessed):
            guessed = input("Enter a valid string: ")

        print(wordle.guess(guessed)[0])
        wordle.solved = wordle.check(guessed)
        wordle.num_guesses += 1

    if wordle.solved:
        print(f"\nWord guess correctly, you did it in {wordle.num_guesses} tries")
    else:
        print("\nThe correct word was: " + wordle.answer)
    
    print("\nPress ctrl + c to end program")


