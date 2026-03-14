import os, sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from wordle_game import WordleGame
from wordle_solver import WordleSolver

def test_grey_letter_filtering():
    solver = WordleSolver()
    solver.grey = {'a'}
    solver.words = {'apple', 'brick', 'pulse'}
    solver.words = solver.remove_greys()

    assert 'apple' not in solver.words

def test_yellow_letters():    
    solver = WordleSolver()
    solver.yellow = [('a', 3)]
    solver.words = {'apple', 'brick', 'pulse'}
    yellow_words = solver.get_yellows()

    assert 'apple' in yellow_words
    assert len(yellow_words) == 1

def test_green_letters():    
    solver = WordleSolver()
    solver.green = [('a', 0)]
    solver.words = {'apple', 'brick', 'pulse'}
    green_words = solver.get_greens()

    assert 'apple' in green_words
    assert len(green_words) == 1

def test_filter():
    solver = WordleSolver()
    solver.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    solver.yellow = [('a', 2), ('n', 3)]
    solver.green = [ ('e', 4), ('a', 0)]
    solver.words = {'apple', 'brick', 'pulse', 'ankle'}
    solver.words, solver.guesses = solver.filter()
    
    assert 'ankle' in solver.guesses
    assert len(solver.guesses) == 1 

def test_filter_no_greens():
    solver = WordleSolver()
    solver.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    solver.yellow = [('a', 2), ('n', 3)]
    solver.green = []
    solver.words = {'apple', 'brick', 'pulse', 'ankle'}
    solver.words, solver.guesses = solver.filter()
    
    assert 'ankle' in solver.guesses
    assert len(solver.guesses) == 1 

def test_filter_no_yellows():
    solver = WordleSolver()
    solver.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    solver.yellow = []
    solver.green = [('k', 2), ('a', 0)]
    solver.words = {'apple', 'brick', 'pulse', 'ankle'}
    solver.words, solver.guesses = solver.filter()
    
    assert 'ankle' in solver.guesses
    assert len(solver.guesses) == 1

def test_filter_no_green_yellow():
    solver = WordleSolver()
    solver.grey = {'p', 'b', 'c', 's'}
    solver.yellow = []
    solver.green = []
    solver.words = {'apple', 'brick', 'pulse', 'ankle'}
    solver.words, solver.guesses = solver.filter()
    
    assert 'ankle' in solver.guesses
    assert len(solver.guesses) == 1

def test_allocate_letters():
    solver = WordleSolver()
    solver.grey, solver.yellow, solver.green = solver.allocate_letters('irate', ['G', 'G', '_', 'Y', 'Y'])

    assert solver.green == [('i', 0), ('r', 1)]
    assert solver.yellow == [('t', 3), ('e', 4)]
    assert solver.grey == {'a'}
