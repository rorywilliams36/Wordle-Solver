import numpy as np 

""" 
Wordle Filter

Functions used to filter out words from word list based on the guess

Green letter G = Letter is in the answer and also the correct position
Yellow Y = Letter is in the word but wrong position
Grey _ = Letter is not in the word

"""


ANSWER = "" # Target word
WORDLE_WORDS = set(np.loadtxt("data/wordlists/words.txt", dtype=str)) # All words available in wordle
WORDS_LIST_LEN = len(WORDLE_WORDS)
WORD_LEN = 5

class WordleFilter:

    def __init__(self, words: set = WORDLE_WORDS):
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

        # Remove grey letters
        self.words = self.remove_greys()

        green_words = self.get_greens()
        yellow_words = self.get_yellows()

        # Gets possible guesses
        if (len(green_words) == 0) and (len(yellow_words) == 0):
            self.guesses = self.words
        elif (len(green_words) == 0) and (len(yellow_words) > 0):
            self.guesses = yellow_words
        elif (len(green_words) > 0) and (len(yellow_words) == 0):
            self.guesses = green_words
        else:
            # Get common words from yellow and green sets by & operation
            self.guesses = green_words & yellow_words

        return self.words, self.guesses

    def get_greens(self):
        """
        Returns a set of words with already correct letters (greens)
        """
        
        green_words = set()
        check = len(self.green)

        for w in self.words:
            # counter to check if word contains all letters in green array
            count = len([l for l, pos in self.green if w[pos] == l])

            # if the word contains all green letters add to array
            if check != 0 and count != 0 and count == check:
                green_words.add(w)

        return green_words

    def get_yellows(self):
        """
        Returns set of words which only contain yellow letters
        """

        check = len(self.yellow)
        yellow_words = set()

        for w in self.words:
            # Counter to check word contains all letters in yellow array
            count = len([l for l, pos in self.yellow if l in w])

            if check != 0 and count != 0 and count == check:
                yellow_words.add(w)

        return yellow_words

    def remove_greys(self):
        ''' Removes all words from the word list that contain grey letters '''
        return set([w for w in self.words if not (set(w) & self.grey)])

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

        self.grey = self.grey - green_set - yellow_set

        return self.grey, self.yellow, self.green

if __name__ == "__main__":
    word_filter = WordleFilter()

    # temp
    word_filter.grey = {'i', 't', 's', 'c', 'h' 'e'}
    word_filter.yellow = []
    word_filter.green = [('a', 2), ('r', 1)]

    word_filter.words, word_filter.guesses = word_filter.filter()

    # scores = word_filter.get_guess_scores()
    # print(word_filter.words)
    print(word_filter.guesses)

