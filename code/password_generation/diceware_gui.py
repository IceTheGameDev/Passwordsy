"""
Called upon opening startup,
this module prepares the diceware frame of the window,
with a set of functions for the graphical part of rolling dice,
getting a password from the diceware wordlist,
and selecting certain words to copy.
"""
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from PIL import ImageTk, Image
import customtkinter

import password_generation.diceware_logic as logic

global number_of_dicerolls
global clear_btn_image
global checkboxes_text_boxes
global widget_text_dict
widget_text_dict = {}


class DicewareToplevel(customtkinter.CTkToplevel):
    """
    This class creates the diceware toplevel window and its contents.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.minsize(1100, 650)
        self.iconbitmap('textures/logo.ico')
        self.title('Diceware')

        self.font_name = 'Roboto'
        self.button_border_width = 2
        self.button_border_colour = 'black'
        self.button_fg_color = 'blue'
        self.button_hover_color = 'gray'
        self.button_columnspan = 10

        self.password_state = 'shown'

        global checkboxes_text_boxes
        checkboxes_text_boxes = {}

        # Give a weight to rows 0 to 15
        i = 0
        while i <= 15:
            self.grid_rowconfigure(i, weight=1, uniform='row')
            i += 1

        # https://stackoverflow.com/questions/75792555/why-is-there-extra-space-after-the-last-column-in-a-tkinter-application
        # That question helped me out a TON!
        # Give a weight to columns 0 to 9
        self.grid_columnconfigure((0, 2, 4, 6, 8), weight=1, uniform="a")
        self.grid_columnconfigure((1, 3, 5, 7, 9), uniform="b")

        self.word_font = customtkinter.CTkFont(family=self.font_name, size=12)
        self.button_font = customtkinter.CTkFont(family=self.font_name, size=24)

        self.output_widgets = []
        self.text_widgets = []

        global number_of_dicerolls
        number_of_dicerolls = 0

        self.roll_dice_button = customtkinter.CTkButton(self, border_width=self.button_border_width,
                                                        border_color=self.button_border_colour, text='ROLL DICE',
                                                        font=self.button_font, fg_color=self.button_fg_color,
                                                        hover_color=self.button_hover_color,
                                                        command=lambda: display_words(logic.roll_dice()))
        self.roll_dice_button.grid(row=0, column=0, columnspan=self.button_columnspan, sticky='n')

        self.copy_menu = tk.Menu(self, tearoff=False)
        self.copy_menu.add_command(label='Copy',
                                   command=lambda: logic.copy_selected_text(self.output_widgets))

        def show_copy_menu(event) -> None:
            """
            Called when the user releases a mouse button on a password label,
            this function uses the Tkinter module to display a contextual menu containing a 'copy' button
            for copying the password to the clipboard on the x and y coordinates of the user's cursor,
            where the y coordinates are adjusted by 30 pixels.

            Parameters
            ----------
            event: tkinter.event
                Gets the coordinates of the mouse cursor when the user releases a mouse button on a password_label.
            """
            self.copy_menu.tk_popup(event.x_root, event.y_root - 30)

        def clear_window():
            """
            This function clears the window of any output widgets.
            """
            global widget_text_dict
            widget_text_dict = {}

            global number_of_dicerolls

            for widget in self.output_widgets:
                widget.destroy()

            self.output_widgets = []
            number_of_dicerolls = 0

            global checkboxes_text_boxes
            checkboxes_text_boxes = {}

        self.clear_button = customtkinter.CTkButton(self, border_width=self.button_border_width,
                                                    border_color=self.button_border_colour, text='CLEAR',
                                                    font=self.button_font, fg_color=self.button_fg_color,
                                                    hover_color=self.button_hover_color,
                                                    command=clear_window)
        self.clear_button.grid(row=1, column=0, columnspan=self.button_columnspan, sticky='n')

        def insert_text(textbox, text):
            """
            Called when the user 'rolls the dice' from the display_words function,
            this function aims to take a customtkinter Textbox,
            insert text into it, and bind it to show a copy pop-up menu when the user right-clicks.
            """
            global widget_text_dict

            textbox.configure(state='normal')
            textbox.delete('1.0', 'end')
            textbox.insert('1.0', text)
            textbox.configure(state='disabled')
            textbox.bind('<Button-3>', show_copy_menu)
            widget_text_dict[textbox] = text

        def display_words(pair):
            """
            Called when the user clicks the 'roll dice' button,
            this function displays the pairs of dice rolls and words to the user.

            Parameters
            ----------
            pair: dict
                Contains the pairs of dice roll numbers and related words according to the dice ware wordlist.
            """
            global number_of_dicerolls
            global checkboxes_text_boxes

            text_height = 1
            text_padx = 10

            if number_of_dicerolls < 35:
                column_to_be_placed_in = (number_of_dicerolls % 5) * 2
                number_of_dicerolls += 1
                (diceroll, word), = pair.items()

                self.diceroll_widget = customtkinter.CTkTextbox(self, font=self.word_font, height=text_height)
                self.diceroll_widget.grid(row=2 + 2 * ((number_of_dicerolls - 1) // 5),
                                          column=column_to_be_placed_in,
                                          pady=(5, 0), padx=text_padx)
                insert_text(self.diceroll_widget, str(diceroll))
                self.output_widgets.append(self.diceroll_widget)
                self.text_widgets.append(self.diceroll_widget)

                self.word_widget = customtkinter.CTkTextbox(self, font=self.word_font, height=text_height)
                self.word_widget.grid(row=3 + 2 * ((number_of_dicerolls - 1) // 5),
                                      column=column_to_be_placed_in,
                                      pady=(0, 5), padx=text_padx)
                insert_text(self.word_widget, word)
                self.output_widgets.append(self.word_widget)
                self.text_widgets.append(self.word_widget)

                self.checkbox = customtkinter.CTkCheckBox(master=self,
                                                          text='',
                                                          checkbox_width=20, width=0,
                                                          checkbox_height=20, fg_color='gray',
                                                          hover_color=('grey', 'white'))
                self.checkbox.grid(row=3 + 2 * ((number_of_dicerolls - 1) // 5), column=column_to_be_placed_in + 1,
                                   sticky='w')
                self.output_widgets.append(self.checkbox)
                checkboxes_text_boxes[self.word_widget] = self.checkbox
                if self.password_state == 'hidden':
                    hide_passwords()
            else:
                answer = tk.messagebox.askquestion('Dice roll limit reached',
                                                   'You have reached the maximum limit of 35 dice rolls. Do you want '
                                                   'to clear the screen?', parent=self)
                if answer == 'yes':
                    clear_window()

        self.copy_button = customtkinter.CTkButton(self, border_width=self.button_border_width,
                                                   border_color=self.button_border_colour, text='COPY SELECTIONS',
                                                   font=self.button_font, fg_color=self.button_fg_color,
                                                   hover_color=self.button_hover_color,
                                                   command=lambda: logic.copy_selections(checkboxes_text_boxes))
        self.copy_button.grid(row=16, column=0, columnspan=self.button_columnspan, pady=10, sticky='n')

        def show_passwords() -> None:
            """
            Called when the user clicks the show button,
            this function shows all passwords.
            """
            global widget_text_dict
            if widget_text_dict != {}:
                for widget, text in widget_text_dict.items():
                    widget.configure(state='normal')
                    widget.insert('0.0', text)
                    widget.configure(state='disabled')
            self.password_state = 'shown'
            self.hide_show_button.configure(text='HIDE PASSWORDS', command=hide_passwords)

        def hide_passwords() -> None:
            """
            Called when the user clicks the hide button,
            this function hides all passwords.
            """
            global widget_text_dict

            if widget_text_dict != {}:
                for widget in self.text_widgets:
                    widget.configure(state='normal')
                    if widget.get('1.0', 'end') != '\n':
                        widget_text_dict[widget] = widget.get('1.0', 'end')
                    widget.delete('0.0', 'end')
                    widget.configure(state='disabled')
            self.password_state = 'hidden'
            self.hide_show_button.configure(text='SHOW PASSWORDS', command=show_passwords)

        self.hide_show_button = customtkinter.CTkButton(self, border_width=self.button_border_width,
                                                        border_color=self.button_border_colour, text='HIDE PASSWORDS',
                                                        font=self.button_font, fg_color=self.button_fg_color,
                                                        hover_color=self.button_hover_color,
                                                        command=hide_passwords)
        self.hide_show_button.grid(row=17, column=0, columnspan=self.button_columnspan, pady=10, sticky='n')

        self.withdraw()
        self.after(200, self.show_icon)

        def close_second_window():
            """
            This function destroys the window when it is closed.
            """
            self.destroy()
            self.master.deiconify()

        self.protocol("WM_DELETE_WINDOW", close_second_window)

    def show_icon(self):
        """
        This function shows the icon of the toplevel window.
        """
        self.deiconify()
        self.iconbitmap('textures/logo.ico')
