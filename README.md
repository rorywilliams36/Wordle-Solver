# Wordle Solver

A Wordle solver that uses **information entropy**, **worst-case minimisation**, and **probability weighting** to find optimal guesses.  
Inspired by Grant Sanderson (3Blue1Brown) youtube videos which uses Information Theory to create a Wordle Solver [1, 2]

- Entropy: To maximise information gain 
- Worst-case: find guesses that reduces the possible answers list the most
- Word Probabilities: more bias towards more common words

Words are scored then ranked by using these metrics in a weighted sum calculation where the weights are largely biased to the entropy value and least biased towards the word probability

Solver averages ~3.5 guesses to find the answer  
Currently there maybe a few cases where the word is guessed >6 guesses

---

## Usage

Install the requirements using `pip install -r requirements.txt` in your terminal

Navigate to the folder that contains this project and run `python main.py`
This file contains arguments to run each part of the code (use `--help` to view)

**First Program Run:**  
`python main.py -gd -wl {guesses, answers, most_common}`  
  
This creates all data needed to run the solver 
The word list used are either:
- `guesses`: all allowed guesses in Wordle (~23000 words)
- `answers`: all previous answer for Wordle (~2300 words)
- `most_common`: (Default Option) most common five letter words (~5750 words)   

*Note that the choice of wordlist can drastically increase the runtime of the program and each time the wordlist is changed the command above must be performed again

---

### Running Wordle Game

To run the game standalone in terminal:  
`py main.py -g -wl {guesses, answers, most_common}`  
You have the option to also set the answer to the game using `-sa`/`--set_answer`

---

### Running the Solver

To run Solver:  
1. First train to find weights using `py main.py -ts {--set_train_iterations 10} -wl {{guesses, answers, most_common}}`
2. Then test using `py main.py -s -wl {guesses, answers, most_common}`

Testing will simulate all possible Wordle games using the selected word list and output the average guesses to find the answer as well as the guess distribution showing the frequency of guesses for each game

You can also use the `-rs` argument to set a number of random samples from the word list to be used in the solver  

*Training is not neccessary as best weights are already in the program

---

### Viewing the Results

To view results run `py results_interface.py`  

---  

## References
[1] Sanderson, G. (2022). [Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA)

[2] Sanderson, G. (2022). [Oh, wait, actually the best Wordle opener is not ‘crane’…](https://www.youtube.com/watch?v=fRed0Xmc2Wg)
