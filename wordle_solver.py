import numpy as np 
from wordle_game import *

""" 
Wordle solver

Green letter = Letter is in the answer and also the correct position
Yellow = Letter is in the word but wrong position
Grey = Letter is not in the word

"""


'''
TODO:

Refactor elimination/get guesses functions
Link to game
Use letter frequencies for best guesses or create scoring system


'''

ANSWER = "" # Target word
WORDLE_WORDS = np.loadtxt("words.txt", dtype=str) # All words able to be answers in wordle

class WordleSolver:

    def __init__(self):
        self.words = WORDLE_WORDS # Avaliable words 
        self.guesses = np.array([]) # Contains best words/guesses
        self.user_inputs = np.array([]) 
        self.green = np.array([]) # Array containing position of green letters [(letter, pos)]
        self.yellow = np.array([]) # Array containing position of yellow letters [(letter, pos)]
        self.grey = np.array([]) # Array containing letters not included in the target/answer word


    def grey_eliminate(self, temp):
        """ 
        Removes words from the array which contain the grey letters
        """
        if temp != None:
            self.grey = np.copy(temp)

        for g in self.grey:
            for w in self.words:
                if w.__contains__(g):
                    self.words = np.delete(self.words, np.where(self.words == w)[0][0])

        return self.words

    def yellow_eliminate(self, temp):
        """
        Removes words from array which contain yellow letters in the stored positions
        """
        if temp != None:
            self.yellow = np.copy(temp)

        for y in self.yellow:
            (l, pos) = y
            pos = int(pos)
            for w in self.words:
                if w.__contains__(l):
                    if w[pos] == l:
                        self.words = np.delete(self.words, np.where(self.words == w)[0][0])

        return self.words

    def get_greens(self, temp):
        """
        Returns a list of words with already correct letters (greens)
        """

        if temp != None:
            self.green = np.copy(temp)

        check = len(self.green)

        for w in self.words:
            count = 0
            for g in self.green:
                (l, pos) = g
                pos = int(pos)
                if w.__contains__(l):
                    if w[pos] == l:
                        count += 1

            if check != 0 and count != 0:
                if count == check:
                    self.guesses = np.append(self.guesses, w)

        return self.guesses


    def get_yellows(self, temp):
        """
        Returns array of words which only contain yellow letters
        Used if no greens are found
        """
        
        if temp != None:
            self.yellow = np.copy(temp)

        check = len(self.yellow)

        for w in self.words:
            count = 0
            for y in self.yellow:
                (l, pos) = y
                if w.__contains__(l):
                    count += 1

            if check != 0 and count != 0:
                if count == check:
                    self.guesses = np.append(self.guesses, w)

        return self.guesses


    def get_guesses(self, temp):
        """
        For some reason won't let me delete items from guesses so I added all words
        I want to a new array then copied it ( self.guesses = np.delete(self.guesses, np.where(xx)[0][0]) )

        From guesses returns an array of the words which contain both yellow and green letters
        """
        new = np.array([])
        if temp != None:
            self.yellow = np.copy(temp)

        check = len(self.yellow)

        for w in self.guesses:
            count = 0
            for y in self.yellow:
                (l, pos) = y
                if w.__contains__(l):
                    count += 1

            if check != 0 and count != 0:
                if count == check:
                    new = np.append(new, w)

        self.guesses = new.copy()
        return self.guesses
        
    def get_next_best(self):
        """
        Gets the best next word to guess
        """

        #for w in self.guesses:



        return None

    def allocate_letters(self):
        """
        Allocates the letters in the current guess to the respective lists
        """
        return None


if __name__ == "__main__":
    solver = WordleSolver()
    game = WordleGame()

    solver.grey = np.array([])
    solver.yellow = np.array([])
    solver.green = np.array([])

    solver.grey_eliminate(None)
    solver.yellow_eliminate(None)

    if len(solver.green) == 0:
        solver.get_yellows(None)
    else:
        solver.get_greens(None)

    solver.get_guesses(None)
        

    print(solver.guesses)