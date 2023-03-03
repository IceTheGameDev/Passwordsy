"""
This module prepares the other_methods_window for the user when they click the 'try other methods...' button.
"""
import tkinter as tk
from tkinter.font import Font
from password_generation import diceware_gui as diceware
from password_generation import sentence_input_gui as sentence_input

other_methods_window = None


def create_other_methods_window() -> None:
    """
    Called upon app startup, this function prepares the other methods window for the user,
    by creating 2 frames: 1 for diceware, and 1 for sentence input.
    """
    title_font = Font(family='Roboto', size=24)

    global other_methods_window
    if other_methods_window is not None and other_methods_window.winfo_exists():
        return

    other_methods_window = tk.Toplevel()
    other_methods_window.geometry('1195x520')
    window_title = 'Try other methods...'

    other_methods_window.iconphoto(False, tk.PhotoImage(file='textures/logo.png'))
    other_methods_window.title(window_title)

    diceware_frame = tk.LabelFrame(other_methods_window, text='Diceware', font=title_font)
    diceware_frame.grid(row=0, column=0, sticky='nsew')

    sentence_input_frame = tk.LabelFrame(other_methods_window, text='Input a sentence', font=title_font)
    sentence_input_frame.grid(row=0, column=1, sticky='nsew')

    diceware.create_diceware_frame(diceware_frame)
    sentence_input.create_sentence_input_frame(sentence_input_frame)

    other_methods_window.grid_rowconfigure(0, weight=1)
    other_methods_window.grid_columnconfigure(0, weight=1)
    other_methods_window.grid_columnconfigure(1, weight=1)
