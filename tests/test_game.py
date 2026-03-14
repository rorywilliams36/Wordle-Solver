import os, sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from wordle_game import WordleGame

def test_win():
    answer = 'irate'
    wordle = WordleGame(answer)
    res = wordle.game('irate')
    assert "".join(wordle.output) == "GGGGG"

def test_no_matches():
    answer = 'plant'
    wordle = WordleGame(answer)
    res = wordle.game('brick')
    assert "".join(wordle.output) == "_____"

def test_all_present():
    answer = 'irate'
    wordle = WordleGame(answer)
    res = wordle.game('tirea')
    assert "".join(wordle.output) == "YYYYY"

def test_multi_letters_in_answer():
    answer = 'paper'
    wordle = WordleGame(answer)
    res = wordle.game('apple')
    assert "".join(wordle.output) == "YYG_Y"

def test_multi_letters_in_guess():
    answer = 'plant'
    wordle = WordleGame(answer)
    res = wordle.game('allee')
    assert "".join(wordle.output) == "YG___"

def test_guessed_letters():
    answer = 'irate'
    wordle = WordleGame(answer)
    res = wordle.game('plant')

    greys = wordle.guessed_letters['Grey']
    yellows = wordle.guessed_letters['Yellow']
    greens = wordle.guessed_letters['Green']

    assert greys == {'P', 'L', 'N'}
    assert yellows == {'T'}
    assert greens == {'A'}

def test_update_yellows_guessed_letters():    
    answer = 'irate'
    wordle = WordleGame(answer)
    wordle.guessed_letters['Yellow'] = {'A'}
    res = wordle.game('plant')

    greys = wordle.guessed_letters['Grey']
    yellows = wordle.guessed_letters['Yellow']
    greens = wordle.guessed_letters['Green']

    assert 'A' not in yellows
    assert greens == {'A'}