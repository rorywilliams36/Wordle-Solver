import os, sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from solver.filters import WordleFilter

def test_grey_letter_filtering():
    word_filter = WordleFilter()
    word_filter.grey = {'a'}
    word_filter.words = {'apple', 'brick', 'pulse'}
    word_filter.words = word_filter.remove_greys()

    assert 'apple' not in word_filter.words

def test_yellow_letters():    
    word_filter = WordleFilter()
    word_filter.yellow = [('a', 3)]
    word_filter.words = {'apple', 'brick', 'pulse'}
    yellow_words = word_filter.get_yellows()

    assert 'apple' in yellow_words
    assert len(yellow_words) == 1

def test_green_letters():    
    word_filter = WordleFilter()
    word_filter.green = [('a', 0)]
    word_filter.words = {'apple', 'brick', 'pulse'}
    green_words = word_filter.get_greens()

    assert 'apple' in green_words
    assert len(green_words) == 1

def test_filter():
    word_filter = WordleFilter()
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = [('a', 2), ('n', 3)]
    word_filter.green = [ ('e', 4), ('a', 0)]
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.words, word_filter.guesses = word_filter.filter()
    
    assert 'ankle' in word_filter.guesses
    assert len(word_filter.guesses) == 1 

def test_filter_no_greens():
    word_filter = WordleFilter()
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = [('a', 2), ('n', 3)]
    word_filter.green = []
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.words, word_filter.guesses = word_filter.filter()
    
    assert 'ankle' in word_filter.guesses
    assert len(word_filter.guesses) == 1 

def test_filter_no_yellows():
    word_filter = WordleFilter()
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = []
    word_filter.green = [('k', 2), ('a', 0)]
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.words, word_filter.guesses = word_filter.filter()
    
    assert 'ankle' in word_filter.guesses
    assert len(word_filter.guesses) == 1

def test_filter_no_green_yellow():
    word_filter = WordleFilter()
    word_filter.grey = {'p', 'b', 'c', 's'}
    word_filter.yellow = []
    word_filter.green = []
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.words, word_filter.guesses = word_filter.filter()
    
    assert 'ankle' in word_filter.guesses
    assert len(word_filter.guesses) == 1

def test_allocate_letters():
    word_filter = WordleFilter()
    word_filter.grey, word_filter.yellow, word_filter.green = word_filter.allocate_letters('irate', ['G', 'G', '_', 'Y', 'Y'])

    assert word_filter.green == {('i', 0), ('r', 1)}
    assert word_filter.yellow == {('t', 3), ('e', 4)}
    assert word_filter.grey == {'a'}
