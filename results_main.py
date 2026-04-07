import tkinter as tk
from tkinter import ttk, Canvas, Checkbutton, messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import numpy as np
import time

import solver.res_utils as r_utils
import solver.data_utils as d_utils

word_list = sorted(set(np.loadtxt("data/wordlists/most_common.txt", dtype=str)))

GUESS_RECORD = d_utils.load_json('guess_record')
GUESS_SCORES = r_utils.load_guess_scores(word_list)


def on_button_click(canvas):
    pass

def display_score_plot(canvas):
    pass

def display_guess_record(canvas):
    pass

def display_distribution(canvas):
    pass

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Wordle Solver Results")

    # Canvas
    canvas = Canvas(root, width=800, height=300, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Make button column
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Pick Word from wordlist
    word_options = list(GUESS_RECORD.keys())[:-2]
    word_options = ttk.Combobox(root, values=word_options)
    word_options.current(0)
    word_options.pack(pady=10)

    # Dropdown to pick guess turn 
    turn_options = ["All", "1", "2", "3", "4", "5", "6", "6+"]
    turn_choice = ttk.Combobox(root, values=turn_options)
    turn_choice.current(0)
    turn_choice.pack(pady=10)

    # Dropdown to pick values 
    score_options = ["Entropy", "Entropy_Ratio", "Worst_Case_Ratio", "Word_Prob", "Score"]
    des_choice = ttk.Combobox(root, values=score_options)
    des_choice.current(0)
    des_choice.pack(pady=10)

    # Buttons
    button1 = tk.Button(root, text="Display Guess Score Plot", command=lambda: on_button_click(canvas, word_options, turn_options, score_options))
    button1.pack(pady=10)

    button2 = tk.Button(root, text="Display Guess Record", command=lambda: on_button_click(canvas, word_options))
    button2.pack(pady=10)

    button3 = tk.Button(root, text="Display Guess Distribution", command=lambda: on_button_click(canvas))
    button3.pack(pady=10)

    button4 = tk.Button(root, text="Display Guess Record with Scores", command=lambda: on_button_click(canvas, word_options))
    button4.pack(pady=10)


    root.mainloop()