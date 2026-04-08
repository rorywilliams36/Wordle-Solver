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


def on_button_click(canvas, button):
    if button == 'Scores':
        pass
    if button == 'Record':
        pass
    if button == 'Distribution':
        display_distribution()

def display_score_plot(canvas, word_choice, turn_choice, score_choice):
    pass

def display_guess_record(canvas, word_choice):
    pass

def display_distribution():
    distribution = GUESS_RECORD['Distribution']
    print(distribution)
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
    word_options = list(GUESS_RECORD.keys())[:-2]
    word_choice = ttk.Combobox(root, values=word_options)
    word_choice.current(0)
    word_choice.pack(pady=10)

    # Dropdown to pick guess turn 
    turn_options = ["All", "1", "2", "3", "4", "5", "6", "6+"]
    turn_choice = ttk.Combobox(root, values=turn_options)
    turn_choice.current(0)
    turn_choice.pack(pady=10)

    # Dropdown to pick values 
    score_options = ["Entropy", "Entropy_Ratio", "Worst_Case_Ratio", "Word_Prob", "Score"]
    score_choice = ttk.Combobox(root, values=score_options)
    score_choice.current(0)
    score_choice.pack(pady=10)

    # Buttons
    # Display score values for each answer given the turn and value (bar chart word on bottom; value on side)
    button1 = tk.Button(root, text="Display Guess Score Plot", command=lambda: on_button_click(canvas, 'Scores'))
    button1.pack(pady=10)

    # displays guess record with thr guess, result and entropy + score for each guess
    # results in the middle with scores and entropies on the side
    button2 = tk.Button(root, text="Display Guess Record", command=lambda: on_button_click(canvas, 'Record'))
    button2.pack(pady=10)

    # bar chart
    button3 = tk.Button(root, text="Display Guess Distribution", command=lambda: display_distribution())
    button3.pack(pady=10)

    root.mainloop()