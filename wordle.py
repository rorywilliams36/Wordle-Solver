import numpy as np 
import os

""" 
Wordle solver

"""

green = np.array([])
yellow = np.array([])
grey = np.array([])

WORDLE_WORDS = np.loadtxt("words.txt", dtype=str)
words_available = np.copy(WORDLE_WORDS)
inputted_words = np.array([])

def grey_eliminate(words, grey):
    """ 
    Returns a list of words which don't contain grey letters
    """

    for g in grey:
        for w in words:
            if w.__contains__(g):
                words = np.delete(words, np.where(words == w)[0][0])

    return words


def yellow_eliminate():
    """
    Returns list of words where letters aren't in the same position of the yellow letters
    Used for creating unlikely guesses (words with multiple of same letters)
    """
    for y in yellow:
        (l, pos) = y
        for w in words:
            if w.__contains__(l):
                for p in pos:
                    if w[p] == l:
                        words = np.delete(words, np.where(words == w)[0][0])
            else:
                next

    return words

def check_word():
    """
    Checks if word is correct
    """
    return None

def check_multi_letter():
    """
    Checks if word contains multiple of same letters
    """
    return None

def get_next_best():
    """
    Gets the best next word to guess
    """
    return None

def allocate_letters():
    """
    Allocates the letters in the current guess to the respective lists
    """
    return None


