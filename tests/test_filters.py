import os, sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from solver.filters import WordleFilter

# Test letter allocation after guess
def test_allocate_letters():
    word_filter = WordleFilter()
    word_filter.grey, word_filter.yellow, word_filter.green = word_filter.allocate_letters('irate', ['G', 'G', '_', 'Y', 'Y'])

    assert word_filter.green == {('i', 0), ('r', 1)}
    assert word_filter.yellow == {('t', 3), ('e', 4)}
    assert word_filter.grey == {'a'}

def test_update_allocation():
    word_filter = WordleFilter()
    word_filter.grey = {'a', 'b', 'c', 'e'}
    word_filter.yellow = {('z', 0)}
    word_filter.green = {('x', 2)}
    word_filter.grey, word_filter.yellow, word_filter.green = word_filter.allocate_letters('irate', ['G', 'G', '_', 'Y', 'Y'])

    assert word_filter.grey == {'a', 'b', 'c'}
    assert word_filter.yellow == {('z', 0), ('t', 3), ('e', 4)}
    assert word_filter.green == {('x', 2), ('i', 0), ('r', 1)}

# Test Counter Constraints
def test_counter_creation():
    word_filter = WordleFilter()
    max_counts, min_counts = word_filter.create_count_contraint('irate', 'GGY__')
    
    assert max_counts == {'i' : 2, 'r' : 2, 'a' : 2, 't' : 0, 'e' : 0}
    assert min_counts == {'i' : 1, 'r' : 1, 'a' : 1}

def test_counter_creation_double_letters():
    word_filter = WordleFilter()
    max_counts, min_counts = word_filter.create_count_contraint('stood', 'GGGG_')
    
    assert max_counts == {'s' : 2, 't' : 2, 'o' : 2, 'd' : 0}
    assert min_counts == {'s' : 1, 't' : 1, 'o' : 2}

def test_update_counters():
    word_filter = WordleFilter()
    curr_max_counts, curr_min_counts = word_filter.create_count_contraint('stock', 'GGG__')

    word_filter.max_counts = {'r': 0, 'a': 0, 'i': 0, 's': 1, 'e': 0}
    word_filter.min_counts = {'s': 1}           

    word_filter.max_counts, word_filter.min_counts = word_filter.update_count_contraints(curr_min_counts, curr_max_counts)

    assert word_filter.max_counts == {'r': 0, 'a': 0, 'i': 0, 's': 1, 'e': 0, 't': 2, 'o': 2, 'c': 0, 'k': 0}
    assert word_filter.min_counts == {'s' : 1, 't' : 1, 'o' : 1}

# Test Filtering
def test_filter_counters():
    word_filter = WordleFilter()

    word_filter.max_counts = {'r': 0, 'a': 0, 'i': 0, 's': 2, 't': 2, 'o': 2, 'c': 0, 'k': 0}
    word_filter.min_counts = {'s' : 1, 't' : 1, 'o' : 1}

    min_not_valid = word_filter.filter_letter_counts('stock') # doesn't contain c
    max_not_valid = word_filter.filter_letter_counts('slash') # contains to many s 's
    single_valid = word_filter.filter_letter_counts('stole') # test double letters
    double_valid = word_filter.filter_letter_counts('stood') #  test single letters

    assert min_not_valid == False
    assert max_not_valid == False
    assert single_valid == True
    assert double_valid == True

def test_filter_no_greens():
    word_filter = WordleFilter()
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = {('a', 2), ('n', 3)}
    word_filter.green = {}
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.pos_answers, _ = word_filter.filter()
    
    assert 'ankle' in word_filter.pos_answers
    assert len(word_filter.pos_answers) == 1 

def test_filter_no_yellows():
    word_filter = WordleFilter()
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = {}
    word_filter.green = {('k', 2), ('a', 0)}
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.pos_answers, _ = word_filter.filter()
    
    assert 'ankle' in word_filter.pos_answers
    assert len(word_filter.pos_answers) == 1

def test_filter_no_green_yellow():
    word_filter = WordleFilter()
    word_filter.grey = {'p', 'b', 'c', 's'}
    word_filter.yellow = {}
    word_filter.green = {}
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.pos_answers, _ = word_filter.filter()
    
    assert 'ankle' in word_filter.pos_answers
    assert len(word_filter.pos_answers) == 1

def test_filter_all_colours():
    word_filter = WordleFilter()
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = {('a', 2), ('n', 3)}
    word_filter.green = {('e', 4), ('a', 0)}
    word_filter.words = {'apple', 'brick', 'pulse', 'ankle'}
    word_filter.pos_answers, _ = word_filter.filter()
    
    assert 'ankle' in word_filter.pos_answers
    assert len(word_filter.pos_answers) == 1 

# All filters together
def test_filter():
    word_filter = WordleFilter()
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = {('a', 2), ('n', 4), ('e', 2)}
    word_filter.green = {('a', 0)}

    word_filter.min_counts = {'a': 1, 'n': 1, 'e': 1}
    word_filter.max_counts = {'i': 0, 'r': 0, 't': 0, 's': 0, 'o': 0, 'u': 0, 'd': 0, 'g': 0,
                                'a': 2, 'n': 2, 'e': 2}

    word_filter.words = {'apple', 'brick', 'pulse', 'ankle', 'annex'}

    word_filter.pos_answers, allowed_guesses = word_filter.filter()

    assert word_filter.pos_answers == {'ankle', 'annex'}
    assert len(word_filter.pos_answers) == 2
    assert allowed_guesses == {'ankle', 'apple', 'annex'}

