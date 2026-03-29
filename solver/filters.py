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
        guesses: Set of words that are possible answers
        green: Set containing position of green letters [(letter, pos)]
        yellow: Set containing position of yellow letters [(letter, pos)]
        grey: Set containing letters not included in the target/answer word
    '''

    def __init__(self, words: set = WORD_LIST):
        self.words = words
        self.guesses = set()
        self.green = set() 
        self.yellow = set()
        self.grey = set()

    def filter(self):
        """ 
        Removes words from the array which contain the invalid letters

        Return:
            guesses = set of words that can be possible answers
            words = set of all available words that can be guessed not containing grey letters
        """

        self.guesses = set()

        self.words = self.remove_greys()
        
        green_check = len(self.green)
        yellow_check = len(self.yellow)

        for word in self.words:
            set_word = set(word)

            valid = True

            # Check Green
            green_count = 0
            for l, pos in self.green:
                if word[pos] != l:
                    valid = False
                    break
                green_count += 1

            if green_count != green_check:
                valid = False

            if not valid:
                continue

            # Check Yellows
            yellow_count = 0
            for l, pos in self.yellow:
                if l not in set_word:
                    valid = False
                    break
                if word[pos] == l:
                    valid = False
                    break
                yellow_count += 1

            if yellow_check != yellow_count:
                valid = False
            
            if not valid: 
                continue

            # Add word if allowed
            if valid:
                self.guesses.add(word)

        return self.guesses, self.words

    def remove_greys(self):
        ''' Returns list of words that dont contain grey letters '''
        return [w for w in self.words if not (set(w) & self.grey)]

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
    word_filter.grey = {'i', 'r', 'e', 'u', 'n', 'd', 's'}
    word_filter.yellow = {('a', 2), ('t', 3), ('o', 2)}
    word_filter.green = {}

    word_filter.guesses. allowed_guesses = word_filter.filter()

    # scores = word_filter.get_guess_scores()
    # print(word_filter.words)
    print(word_filter.guesses)

