import numpy as np
import random

class WordleGame:

    def __init__(self, answer: str = None, sim: bool = False):
        self.answer = answer
        self.word_list = np.loadtxt('words.txt', dtype = str)
        self.guesses = np.array([])
        self.sim = sim
        self.solved = False
        self.guesses_left = 0

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


if __name__ == "__main__":
    wordle = WordleGame()
    if wordle.answer == None:
        wordle.answer = wordle.pickRandomWord()

    while not wordle.solved and wordle.guesses_left < 6:
        guessed = input("Enter a word: ")
        print(wordle.guess(guessed)[0])
        wordle.solved = wordle.check(guessed)
        wordle.guesses_left += 1

    if wordle.solved:
        print(f"\nWord guess correctly, you did it in {wordle.guesses_left} tries")
    else:
        print("The correct word was: " + wordle.answer)


