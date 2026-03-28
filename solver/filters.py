import numpy as np 

""" 
Wordle Filter

Functions used to filter out words from word list based on the guess

Green letter G = Letter is in the answer and also the correct position
Yellow Y = Letter is in the word but wrong position
Grey _ = Letter is not in the word

"""


ANSWER = "" # Target word
WORD_LIST = set(np.loadtxt("data/wordlists/words.txt", dtype=str)) # All words available in wordle
WORDS_LIST_LEN = len(WORD_LIST)
WORD_LEN = 5

class WordleFilter:

    def __init__(self, words: set = WORD_LIST):
        self.words = words # Avaliable words that can be used
        self.guesses = set() # Contains all possible guesses
        self.green = set() # Array containing position of green letters [(letter, pos)]
        self.yellow = set() # Array containing position of yellow letters [(letter, pos)]
        self.grey = set() # Set containing letters not included in the target/answer word

    def filter(self):
        """ 
        Removes words from the array which contain the invalid letters

        Return:
            guesses = set of words that contain yellow and green letters
            words = set of all available words that can be guessed not containing grey letters
        """

        self.guesses = set()

        for word in self.words:
            valid = True
            for l, pos in self.green:
                if word[pos] != l:
                    valid = False
                    break
            if not valid:
                continue

            for l, pos in self.yellow:
                if (l not in set(word)):
                    valid = False
                    break
                if word[pos] == l:
                    valid = False
                    break
            if not valid: 
                continue

            for l in self.grey:
                if l in word:
                    valid = False
                    break
    
            if valid:
                self.guesses.add(word)
        return self.guesses

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

    word_filter.guesses = word_filter.filter()
    new_guesses = word_filter.new_filter()

    # scores = word_filter.get_guess_scores()
    # print(word_filter.words)
    print(word_filter.guesses)
    print(new_guesses)

