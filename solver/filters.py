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
WORD_SCORES = np.load("data/word_scores.npy", allow_pickle=True).tolist() 

class WordleFilter:

    def __init__(self):
        self.words = WORDLE_WORDS # Avaliable words that can be used
        self.guesses = set() # Contains all possible guesses
        self.green = [] # Array containing position of green letters [(letter, pos)]
        self.yellow = [] # Array containing position of yellow letters [(letter, pos)]
        self.grey = set() # Set containing letters not included in the target/answer word

    def filter(self):
        """ 
        Removes words from the array which contain the invalid letters
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
        '''
        for i in range(WORD_LEN):
            if result[i] == 'G':
                self.green.append((guessed_word[i], i))
            elif result[i] == 'Y':
                self.yellow.append((guessed_word[i], i))
            else:
                self.grey.add(guessed_word[i])

        return self.grey, self.yellow, self.green

if __name__ == "__main__":
    word_filter = WordleFilter()

    # temp
    word_filter.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    word_filter.yellow = [('a', 2), ('n', 3)]
    word_filter.green = [('a', 0), ('e', 4)]

    word_filter.words, word_filter.guesses = word_filter.filter()

    # scores = word_filter.get_guess_scores()
    print(scores)
    # print(word_filter.words)
    print(word_filter.guesses)

