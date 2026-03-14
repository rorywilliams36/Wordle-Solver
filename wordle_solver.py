import numpy as np 
from wordle_game import WordleGame

""" 
Wordle solver

Green letter G = Letter is in the answer and also the correct position
Yellow Y = Letter is in the word but wrong position
Grey _ = Letter is not in the word

"""


ANSWER = "" # Target word
WORDLE_WORDS = set(np.loadtxt("data/wordlists/words.txt", dtype=str)) # All words available in wordle
WORDS_LIST_LEN = len(WORDLE_WORDS)
WORD_LEN = 5
WORD_SCORES = np.load("data/word_scores.npy", allow_pickle=True).tolist() 

class WordleSolver:

    def __init__(self):
        self.words = WORDLE_WORDS # Avaliable words that can be used
        self.guesses = set() # Contains all possible guesses
        self.user_inputs = []
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
        if (len(green_words) == 0) & (len(yellow_words) == 0):
            self.guesses = self.words
        if (len(green_words) == 0) & (len(yellow_words) > 0):
            self.guesses = yellow_words
        if (len(green_words) > 0) & (len(yellow_words) == 0):
            self.guesses = green_words
        else:
            # Get common words from yellow and green sets by & operation
            print('')
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


    def get_guess_scores(self):
        """
        Returns array of tuples containing the guess and its score

        TODO:
        Base scores
        More vowels ++
        More common ++
        Multi letters --
        """
        scores = []
        for g in self.guesses:
            scores.append((g, WORD_SCORES[g]))

        scores = sorted(scores, key=lambda tup: tup[1], reverse=True)

        return scores

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


if __name__ == "__main__":
    solver = WordleSolver()
    wordle = WordleGame()

    # temp
    solver.grey = {'i', 'r', 't', 's', 'o', 'u', 'd', 'g'}
    solver.yellow = [('a', 2), ('n', 3)]
    solver.green = [ ('e', 4), ('a', 0)]

    solver.words, solver.guesses = solver.filter()

    scores = solver.get_guess_scores()
    print(scores)
    # print(solver.words)
    print(solver.guesses)

