import tkinter as tk
from tkinter import ttk, Canvas, Checkbutton, messagebox
from PIL import Image, ImageTk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

import solver.res_utils as r_utils
import solver.data_utils as d_utils

word_list = sorted(set(np.loadtxt("data/wordlists/most_common.txt", dtype=str)))

GUESS_RECORD = d_utils.load_json('guess_record')
GUESS_SCORES = r_utils.load_guess_scores(word_list)

score_idx = ["_", "Entropy", "Entropy_Ratio", "Worst_Case_Ratio", "Word_Prob", "Score"]
colors = {'_': "#787c7e", 'Y': "#c9b458", 'G': "#6aaa64" }

def display_score_plot(canvas, word_choice, turn_choice, score_choice):
    ''' Displays bar chart showing relevant score metrics with the best possible guesses given the answer and turn number '''
    word, turn, score = get_choices(word_choice, turn_choice, score_choice)
    game_scores = GUESS_SCORES[word]

    if turn >= len(game_scores):
        turn = len(game_scores)-1

    turn_scores = game_scores[turn]

    x_axis = [i[0] for i in turn_scores]
    y_axis = [i[score] for i in turn_scores]

    canvas.delete('all')

    # Create a Matplotlib figure
    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(x_axis, y_axis)

    ax.set_title(f'Guess Scores for Answer: {word}, Guess Number: {turn+1}')
    ax.set_xlabel(f'Top 10 Potential Guesses')
    ax.set_ylabel(f'{score_idx[score]}')
    ax.tick_params(axis='x', rotation=45)

    plot_canvas = FigureCanvasTkAgg(fig, master=canvas)
    plot_canvas.draw()

    canvas.create_window(0, 0, anchor="nw",
                                window=plot_canvas.get_tk_widget())

def display_guess_record(canvas, word_choice):
    ''' Diplays the solvers guesses with metrics for the wordle game given the answer '''
    word = word_choice.get()
    guesses = GUESS_RECORD[word]
    num_guesses = len(guesses)

    # Get the scores for the guessed words in the guess record
    guesses_scores = [scores[0][-1] for scores in GUESS_SCORES[word]]
    guesses_entropies = [scores[0][1] for scores in GUESS_SCORES[word]]

    TILE_SIZE = 60
    PADDING = 10
    Y_OFFSET = 25

    canvas.delete('all')
    for row in range(len(guesses)):
        for col in range(5):
            # Get the guess and the result
            guess = guesses[row]['Guess']
            result = guesses[row]['Result']

            # Get letter and its result
            letter = guess[col].upper()
            letter_colour = result[col]

            x1 = col * (TILE_SIZE + PADDING) + PADDING
            y1 = row * (TILE_SIZE + PADDING) + PADDING + Y_OFFSET
            x2 = x1 + TILE_SIZE
            y2 = y1 + TILE_SIZE

            # Wordle Grid
            canvas.create_rectangle(x1, y1, x2, y2, fill=colors[letter_colour], outline="")

            canvas.create_text(
                (x1 + x2)//2,
                (y1 + y2)//2,
                text=letter,
                fill="white" if letter else "black",
                font=("Helvetica", 20, "bold")
            )

        # Score + Entropy columns
        score_x = 5 * (TILE_SIZE + PADDING) + 20
        if row < 6:
            canvas.create_text(
                score_x,
                (y1 + y2)//2,
                text=f"{guesses_entropies[row]:.4f}",
                anchor="w",
                font=("Helvetica", 14)
            )

        entropy_x = score_x + 70
        if row < 6:
            canvas.create_text(
                entropy_x,
                (y1 + y2)//2,
                text=f"{guesses_scores[row]:.4f}",
                anchor="w",
                font=("Helvetica", 14)
            )

    header_y = PADDING // 2 + Y_OFFSET

    canvas.create_text(
        5 * (TILE_SIZE + PADDING) + 20,
        header_y,
        text="Entropy",
        anchor="w",
        font=("Helvetica", 12, "bold")
    )

    canvas.create_text(
        5 * (TILE_SIZE + PADDING) + 100,
        header_y,
        text="Score",
        anchor="w",
        font=("Helvetica", 12, "bold")
    )


def display_distribution():
    ''' Displays the guess distribution of the solver '''
    distribution = GUESS_RECORD['Distribution']
    canvas.delete('all')

    # Create a Matplotlib figure
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar([0,1,2,3,4,5,6,7,8,9], distribution)

    ax.set_title('Guess Occurences')
    ax.set_xlabel('Guess Num')
    ax.set_ylabel('Occurences')
    ax.set_yticks([i for i in range(max(distribution)+1)])
    ax.set_xticks([0,1,2,3,4,5,6,7,8,9])

    plot_canvas = FigureCanvasTkAgg(fig, master=canvas)
    plot_canvas.draw()

    canvas.create_window(0, 0, anchor="nw",
                                window=plot_canvas.get_tk_widget())

def get_choices(word_choice, turn_choice, score_choice):
    ''' Gets the choices from the dropdown '''
    word = word_choice.get()
    turn = int(turn_choice.get())-1
    score = score_idx.index(score_choice.get())
    return word, turn, score


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Wordle Solver Results")

    # Canvas
    canvas = tk.Canvas(root, width=500, height=500, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    # Make button column
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Pick Word from wordlist
    word_options = sorted(list(GUESS_RECORD.keys())[:-2])
    word_choice = ttk.Combobox(root, values=word_options)
    word_choice.current(0)
    word_choice.pack(pady=10)

    # Dropdown to pick guess turn 
    turn_options = ["1", "2", "3", "4", "5", "6"]
    turn_choice = ttk.Combobox(root, values=turn_options)
    turn_choice.current(0)
    turn_choice.pack(pady=10)

    # Dropdown to pick score values 
    score_options = ["Entropy", "Entropy_Ratio", "Worst_Case_Ratio", "Word_Prob", "Score"]
    score_choice = ttk.Combobox(root, values=score_options)
    score_choice.current(0)
    score_choice.pack(pady=10)

    # Buttons
    # Display score values for each answer given the turn and value
    button1 = tk.Button(root, text="Display Guess Score Plot", command=lambda: display_score_plot(canvas, word_choice, turn_choice, score_choice))
    button1.pack(pady=10)

    # displays guess record with thr guess, result and entropy + score for each guess
    button2 = tk.Button(root, text="Display Guess Record", command=lambda: display_guess_record(canvas, word_choice))
    button2.pack(pady=10)

    # bar chart
    button3 = tk.Button(root, text="Display Guess Distribution", command=lambda: display_distribution())
    button3.pack(pady=10)

    root.mainloop()