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

'''

ANSWER = "" # Target word
WORDLE_WORDS = np.loadtxt("data/words.txt", dtype=str) # All words able to be answers in wordle
WORD_SCORES = np.load("data/word_scores.npy", allow_pickle=True).tolist() 

class WordleSolver:

    def __init__(self):
        self.words = WORDLE_WORDS # Avaliable words 
        self.guesses = np.array([]) # Contains best words/guesses
        self.user_inputs = np.array([]) 
        self.green = [] # Array containing position of green letters [(letter, pos)]
        self.yellow = [] # Array containing position of yellow letters [(letter, pos)]
        self.grey = [] # Array containing letters not included in the target/answer word


    def filter(self):
        """ 
        Removes words from the array which contain the invalid letters
        """

        # Removes grey letters
        for g in self.grey:
            for w in self.words:
                if w.__contains__(g):
                    self.words = np.delete(self.words, np.where(self.words == w)[0][0])

        # Removes yellow letters
        for y in self.yellow:
            (l, pos) = y
            for w in self.words:
                if w.__contains__(l):
                    if w[int(pos)] == l:
                        self.words = np.delete(self.words, np.where(self.words == w)[0][0])

        return self.words

    def get_greens(self):
        """
        Returns a list of words with already correct letters (greens)
        """

        check = len(self.green)

        for w in self.words:
            count = 0
            for g in self.green:
                (l, pos) = g
                if w[int(pos)] == l:
                    count += 1

            if check != 0 and count != 0 and count == check:
                self.guesses = np.append(self.guesses, w)

        return self.guesses


    def get_yellows(self):
        """
        Returns array of words which only contain yellow letters
        """

        check = len(self.yellow)

        for w in self.words:
            count = 0
            for y in self.yellow:
                (l, pos) = y
                if w.__contains__(l):
                    count += 1

            if check != 0 and count != 0 and count == check:
                self.guesses = np.append(self.guesses, w)

        return self.guesses


    def get_guesses(self):
        """
        For some reason won't let me delete items from guesses so I added all words I want to a new array then copied it ( self.guesses = np.delete(self.guesses, np.where(xx)[0][0]) )

        From guesses returns an array of the words which contain both yellow and green letters
        """
        new = np.array([])
        check = len(self.yellow)

        for w in self.guesses:
            count = 0
            for y in self.yellow:
                (l, pos) = y
                if w.__contains__(l):
                    count += 1

            if check != 0 and count != 0 and count == check:
                    new = np.append(new, w)

        self.guesses = new.copy()
        return self.guesses
        
    def get_guess_scores(self):
        """
        Returns array of tuples containing the guess and its score

        TODO:
        Base scores
        More vowels ++
        More common ++
        Multi letters --
        """
        scores = []
        for g in self.guesses:
            scores.append((g, WORD_SCORES[g]))

        scores = sorted(scores, key=lambda tup: tup[1], reverse=True)
        #print(scores)

        return scores

    def allocate_letters(self, guessed):

        for i in range(0, 5):
            if self.output[i] == 'G':
                self.green.append((guessed[i], i))
            elif output[i] == 'Y':
                self.yellow.append((guessed[i], i))
            else:
                self.grey.append(guessed[i])

        return green, yellow, grey


def simulate():
    first = 'irate'
    

if __name__ == "__main__":
    solver = WordleSolver()
    wordle = WordleGame()

    solver.grey = ['a', 't', 'r', 'o', 'n', 'd']
    solver.yellow = [('s', 0), ('u', 2)]
    solver.green = [ ('e', 4)]

    solver.filter()

    if len(solver.green) == 0:
        solver.get_yellows()
    else:
        solver.get_greens()

    solver.get_guesses()
    scores = solver.get_guess_scores()
    print(scores)
    print(solver.guesses)

    # solver.green, solver.yellow, solver.grey = allocate_letters(['!', '!', '_', '%', '_'], "irate", solver.green, solver.yellow, solver.grey)

