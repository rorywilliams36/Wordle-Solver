import numpy as np 
import os
import tkinter

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

def grey_eliminate(words, grey):
    """ 
    Returns a list of words which don't contain grey letters
    """
    for g in grey:
        for w in words:
            if w.__contains__(g):
                words = np.delete(words, np.where(words == w)[0][0])

    return words

def yellow_eliminate(words, yellow):
    """
    Returns list of words where letters aren't in the same position of the yellow letters
    Used for creating unlikely guesses (words with multiple of same letters)
    """
    for y in yellow:
        (l, pos) = y
        pos = int(pos)
        for w in words:
            if w.__contains__(l):
                if w[pos] == l:
                    words = np.delete(words, np.where(words == w)[0][0])

    return words

def get_greens(words, green):
    """
    Returns a list of words with already correct letters (greens)
    """
    guesses = np.array([])    
    check = len(green)

    for w in words:
        count = 0
        for g in green:
            (l, pos) = g
            pos = int(pos)
            if w.__contains__(l):
                if w[pos] == l:
                    count += 1

        if check != 0 and count != 0:
            if count == check:
                guesses = np.append(guesses, w)

    return guesses

def get_yellows(words, yellow):
    """
    Returns list with words that contain yellow letters regardless of the letters position
    """
    guesses = np.array([])    
    check = len(yellow)

    for w in words:
        count = 0
        for y in yellow:
            (l, pos) = y
            if w.__contains__(l):
                count += 1

        if check != 0 and count != 0:
            if count == check:
                guesses = np.append(guesses, w)

    return guesses

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

# 11/08 Wordle "HELLO"
# words = grey_eliminate(WORDLE_WORDS, np.array(['i', 'r', 'a', 't', 'f', 'u', 's', 'w']))
# words = yellow_eliminate(words, np.array([('e', 4), ('o', 1), ('h', 1), ('o', 2)]))
# guesses = get_greens(words, np.array([('l', 3)]))
# guesses = get_yellows(guesses, np.array([('e', 4), ('o', 1), ('h', 1), ('o', 2)]))

