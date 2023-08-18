import numpy as np 
import os

from wordle_game import *

""" 
Wordle solver
"""

ANSWER = "" # Target word

green = np.array([]) # Contains tuple (letter, position) of correct letters in the correct position
yellow = np.array([]) # contains tuple ^ of correct letters and incorrect position
grey = np.array([]) # Contains characters which aren't included in the target word

WORDLE_WORDS = np.loadtxt("words.txt", dtype=str) # All words able to be answers in wordle
words_available = np.copy(WORDLE_WORDS)
inputted_words = np.array([]) # Tracks user's guesses

class WordleSolver:

    def __init__(self):
        self.words = WORDLE_WORDS
        self.guesses = np.array([])
        self.inputted_words = np.array([])
        self.green = np.array([])
        self.yellow = np.array([])
        self.grey = np.array([])


    def grey_eliminate(self, temp):
        """ 
        Returns a list of words which don't contain grey letters
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
        Returns list of words where letters aren't in the same position of the yellow letters
        Used for creating unlikely guesses (words with multiple of same letters)
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
        Returns list with words that contain yellow letters regardless of the letters position
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

    def check_multi_letter(self):
        """
        Checks if word contains multiple of same letters
        """
        return None

    def get_next_best(self):
        """
        Gets the best next word to guess
        """
        return None

    def allocate_letters(self):
        """
        Allocates the letters in the current guess to the respective lists
        """
        return None

# 11/08 Wordle "HELLO"
# words = grey_eliminate(WORDLE_WORDS, np.array(['i', 'r', 'a', 't', 'f', 'u', 's', 'w']))
# words = yellow_eliminate(words, np.array([('e', 4), ('o', 1), ('h', 1), ('o', 2)]))
# guesses = get_greens(words, np.array([('l', 3)]))
# guesses = get_yellows(guesses, np.array([('e', 4), ('o', 1), ('h', 1), ('o', 2)]))

if __name__ == "__main__":
    solver = WordleSolver()
    solver.grey = np.array(['i', 'r', 'a', 't', 'f', 'u', 's', 'w'])
    solver.yellow = np.array([('e', 4), ('o', 1), ('h', 1), ('o', 2)])
    solver.green = np.array([('l', 3)])

    solver.words = solver.grey_eliminate(None)
    solver.words = solver.yellow_eliminate(None)
    solver.guesses = solver.get_greens(None)
    solver.guesses = solver.get_yellows(None)

    print(solver.guesses)