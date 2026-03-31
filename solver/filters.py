from collections import Counter
import numpy as np

""" 
Wordle Filter

This module contains functions used to filter out words from word list based on the guess

Green letter G = Letter is in the answer and also the correct position
Yellow Y = Letter is in the word but wrong position
Grey _ = Letter is not in the word

"""

ANSWER = "" # Target word
WORD_LIST = set(np.loadtxt("data/wordlists/words.txt", dtype=str)) # All words available in wordle
WORDS_LIST_LEN = len(WORD_LIST)
WORD_LEN = 5

class WordleFilter:
    '''
    Wordle Filter Class
    Contains relevant functions to filter the word lists given the grey, yellow and green letters

    Attributes:
        words: array of words that are possible guesses
        pos_answers: Set of words that are possible answers
        green: Set containing position of green letters [(letter, pos)]
        yellow: Set containing position of yellow letters [(letter, pos)]
        grey: Set containing letters not included in the target/answer word
    '''

    def __init__(self, words: set = WORD_LIST):
        self.words = words
        self.pos_answers = set()
        self.green = set() 
        self.yellow = set()
        self.grey = set()
        self.min_counts = {}
        self.max_counts = {}

    def filter(self):
        """ 
        Removes words from the array which contain the invalid letters

        Return:
            guesses = set of words that can be possible answers
            words = set of all available words that can be guessed not containing grey letters
        """

        self.pos_answers = set()

        self.words = self.remove_greys()
        
        for word in self.words:
            set_word = set(word)
            valid = True

            # Check Green
            for l, pos in self.green:
                if word[pos] != l:
                    valid = False
                    break

            if not valid:
                continue

            # Check Yellows
            for l, pos in self.yellow:
                if l not in set_word:
                    valid = False
                    break
                if word[pos] == l:
                    valid = False
                    break
            
            if not valid: 
                continue
            
            # FIlter based on letter counts
            valid = self.filter_word_counts(word)

            # Add word if allowed
            if valid:
                self.pos_answers.add(word)
        return self.pos_answers, self.words

    def remove_greys(self):
        ''' Returns list of words that dont contain grey letters '''
        return [w for w in self.words if not (set(w) & self.grey)]

    def filter_word_counts(self, word):
        ''' Filters word based on letter counts '''
        word_counts = Counter(word)
        for l in self.min_counts:
            if word_counts[l] < self.min_counts[l]:
                return False
        for l in self.max_counts:
            if word_counts[l] > self.max_counts[l]:
                return False
        return True

    def update_count_contraints(self, min_counts, max_counts):
        ''' Updates the min/max counters after a guess has been submitted '''
        for l in min_counts:
            self.min_counts[l] = max(self.min_counts.get(l, 0), min_counts[l])

        for l in max_counts:
            self.max_counts[l] = min(self.max_counts.get(l, 5), max_counts[l])
            # if min count of letter is bigger than max count
            if l in self.min_counts:
                if self.max_counts[l] < self.min_counts[l]:
                    self.max_counts[l] = self.min_counts[l]

        return self.max_counts, self.min_counts

    def create_count_contraint(self, guessed_word, result):
        ''' 
        Creates counters showing the max/min occurences a letter can have in a word
        Used to avoid cases where a word with a double letter is guessed and other words 
        with double letters are not removed from the possible answer list
        '''
        guessed_word_counts = Counter(guessed_word)
        min_counts = {}
        max_counts = {}
        word_len = len(guessed_word)

        # Gets the minimum count for letters in the result using yellows and greens
        for i, res in enumerate(result):
            if res in ('G', 'Y'):
                min_counts[guessed_word[i]] = min_counts.get(guessed_word[i], 0) + 1

        # Get number of guessed letters correct
        sum_min_counts = sum(min_counts.values())

        # Get max occurences a letter can have
        for letter in guessed_word_counts:
            min_letter_count = min_counts.get(letter, 0)

            # gets occurences of the letter being grey in the result
            # if a letter is grey and green/yellow there cant be more occurences of the letter
            grey_count = sum(1 for i, res in enumerate(result) if ((res == '_') and (guessed_word[i] == letter)))

            # if letter is green/yellow and grey set max_count to min value
            if grey_count > 0:
                max_counts[letter] = min_letter_count
            # Set upper bound
            # can be at most 5 of same letter but unlikely
            else:
                max_counts[letter] = word_len-len(min_counts.values())

        return max_counts, min_counts


    def allocate_letters(self, guessed_word, result):
        '''
        Function to allocate letters in the last guess into respective
        arrays/sets based on the result of the gues

        Args:
            guessed_word: string of the current word guessed
            result: result using the guessed_word

        Return:
            grey: set of letters that are set to grey in result
            yellow: set of yellow letters as (letter, index)
            green: set of green letters (letter, index)
        '''
        for i in range(WORD_LEN):
            if result[i] == 'G':
                self.green.add((guessed_word[i], i))
            elif result[i] == 'Y':
                self.yellow.add((guessed_word[i], i))
            else:
                self.grey.add(guessed_word[i])
        
        green_set = {c for c, _ in self.green}
        yellow_set = {c for c, _ in self.yellow}

        # letters cannot be grey and yellow/green at the same time
        self.grey = self.grey - green_set - yellow_set

        return self.grey, self.yellow, self.green


if __name__ == "__main__":
    word_filter = WordleFilter()

    # temp
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = [('a', 2), ('n', 4), ('e', 2)]
    word_filter.green = [('a', 0)]

    word_filter.min_counts = {'a': 1, 'n': 1, 'e': 1}
    word_filter.max_counts = {'i': 0, 'r': 0, 't': 0, 's': 0, 'o': 0, 'u': 0, 'd': 0, 'g': 0,
                                'a': 2, 'n': 2, 'e': 2}

    word_filter.words = {'apple', 'brick', 'pulse', 'ankle', 'annex'}

    word_filter.pos_answers, allowed_guesses = word_filter.filter()
    print(allowed_guesses)

