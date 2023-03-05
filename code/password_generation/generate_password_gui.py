"""
Called upon app startup,
this module prepares the GUI for password generation
"""
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from PIL import ImageTk, Image
import customtkinter

from password_generation import generate_password_logic as logic
from password_generation import other_methods_gui as other

password_width = 100
password_height = 1
password_border_width = 0
password_font = 'Consolas 11'

invalid_input_error = 'An error occurred. Try again with a whole number between 4 and 100.'
no_character_set_error = 'An error occurred. Try again with at least 1 character set.'
double_error = 'An error occurred. Try again with at least 1 character set and a whole number between 4 and 100.'

global input_box
global copy_menu
global passwords
global show_hide_all_button
global try_other_methods_btn_image
global show_all_btn_image
global hide_all_btn_image
global show_btn_image
global hide_btn_image
global copy_btn_image
global done_btn_image


class PasswordGenerationFrame(customtkinter.CTkFrame):
    """
    Called upon starting the program,
    this class uses the Custom Tkinter module to create a GUI frame,
    used to generate passwords with various options for customisation
    (length and character sets),
    and serves as a hub for all other password generation functions.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        title_font = Font(family='Roboto', size=24)
        section_title_font = Font(family='Roboto', size=16)
        description_font = Font(family='Roboto', size=12)

        global passwords
        passwords = []

        global try_other_methods_btn_image
        try_other_methods_btn_image = ImageTk.PhotoImage(Image.open('textures/try_other_methods_btn.png'))

        global show_all_btn_image
        show_all_btn_image = ImageTk.PhotoImage(Image.open('textures/show_all_btn.png'))

        global hide_all_btn_image
        hide_all_btn_image = ImageTk.PhotoImage(Image.open('textures/hide_all_btn.png'))

        global show_btn_image
        show_btn_image = ImageTk.PhotoImage(Image.open('textures/show_btn.png'))

        global hide_btn_image
        hide_btn_image = ImageTk.PhotoImage(Image.open('textures/hide_btn.png'))

        global copy_btn_image
        copy_btn_image = ImageTk.PhotoImage(Image.open('textures/copy_btn.png'))

        global done_btn_image
        done_btn_image = ImageTk.PhotoImage(Image.open('textures/done_btn.png'))

        self.password_label_1 = tk.Text(self, width=password_width, height=password_height,
                                        borderwidth=password_border_width, font=password_font)
        self.password_label_2 = tk.Text(self, width=password_width, height=password_height,
                                        borderwidth=password_border_width, font=password_font)
        self.password_label_3 = tk.Text(self, width=password_width, height=password_height,
                                        borderwidth=password_border_width, font=password_font)
        self.password_label_4 = tk.Text(self, width=password_width, height=password_height,
                                        borderwidth=password_border_width, font=password_font)
        self.password_labels = [self.password_label_1, self.password_label_2,
                                self.password_label_3, self.password_label_4]

        def clear_text_label(label):
            """
            Called when the user clicks one of the hide buttons,
            this function deletes all content of the specific label.

            Parameters
            ----------
            label: tk.Text
                The text label to be cleared.
            """
            label.configure(state='normal')
            label.delete('1.0', 'end')
            label.configure(state='disabled')

        def show_password(index, button) -> None:
            """
            Called when the user clicks one of the 4 show buttons,
            this function displays the specific password through the show_text function,
            and changes the specific button to a hide button.

            Parameters
            ----------
            index: int
                The number of the button that was clicked.
            button: tk.Button
                The button that was clicked.
            """
            global passwords
            show_text(self.password_labels[index], passwords[index])

            # Check if there is any content in all labels by checking the length (the length of an empty label is 1)
            if len(self.password_labels[0].get('1.0', 'end')) != 1 \
                    and len(self.password_labels[1].get('1.0', 'end')) != 1 \
                    and len(self.password_labels[2].get('1.0', 'end')) != 1 \
                    and len(self.password_labels[3].get('1.0', 'end')) != 1:
                self.show_hide_all_slider.set(1)

            button.configure(image=hide_btn_image, borderwidth=0, command=lambda: hide_password(index, button))

        def hide_password(index, button) -> None:
            """
            Called when the user clicks one of the 4 hide buttons,
            this function clears the specific password_label through the clear_text_label function,
            and changes the specific button to a show_button.

            Parameters
            ----------
            index: int
                The number of the button that was clicked.
            button: tk.Button
                The button that was clicked.
            """
            clear_text_label(self.password_labels[index])

            # Check if there is no content in no label by checking the length (the length of an empty label is 1)
            if len(self.password_labels[0].get('1.0', 'end')) == 1 \
                    and len(self.password_labels[1].get('1.0', 'end')) == 1 \
                    and len(self.password_labels[2].get('1.0', 'end')) == 1 \
                    and len(self.password_labels[3].get('1.0', 'end')) == 1:
                self.show_hide_all_slider.set(0)

            button.configure(image=show_btn_image, command=lambda: show_password(index, button))

        def run_function_based_on_slider_value(value) -> None:
            """
            Called when the user moves the slider,
            this function checks what function to run based on the slider's value:
            if it is 0, it runs hide_all_passwords(), if it is 1, it runs show_all_passwords.

            Parameters
            ----------
            value: float
                The slider's value
            """
            if value == 0:
                hide_all_passwords()
            elif value == 1:
                show_all_passwords()

        def show_all_passwords() -> None:
            """
            Called when the user clicks the 'show all' button,
            this function goes through each password_label,
            inserts the specific password inside of it through the show_text function,
            and changes the button into a hide all button.
            """
            for index, button in enumerate(self.show_hide_buttons):
                show_password(index, button)

        def hide_all_passwords() -> None:
            """
            Called when the user clicks the 'hide all' button,
            this function goes through each password_label,
            and clears it.
            """
            for index, button in enumerate(self.show_hide_buttons):
                hide_password(index, button)

        self.show_hide_button_1 = tk.Button(self, image=show_btn_image, borderwidth=0,
                                            command=lambda: show_password(0, show_hide_button_1))
        self.show_hide_button_2 = tk.Button(self, image=show_btn_image, borderwidth=0,
                                            command=lambda: show_password(1, show_hide_button_2))
        self.show_hide_button_3 = tk.Button(self, image=show_btn_image, borderwidth=0,
                                            command=lambda: show_password(2, show_hide_button_3))
        self.show_hide_button_4 = tk.Button(self, image=show_btn_image, borderwidth=0,
                                            command=lambda: show_password(3, show_hide_button_4))
        self.show_hide_buttons = [self.show_hide_button_1, self.show_hide_button_2,
                                  self.show_hide_button_3, self.show_hide_button_4]
        self.show_hide_all_slider = tk.Scale(self, from_=0, to=1, orient='horizontal',
                                             command=lambda value:
                                             run_function_based_on_slider_value(self.show_hide_all_slider.get()),
                                             bd=1, fg='#F0F0F0', width=20, sliderlength=49, borderwidth=0,
                                             sliderrelief='flat', activebackground='blue')

        self.hide_label = tk.Label(self, text='Hide', font=description_font)
        self.show_label = tk.Label(self, text='Show', font=description_font)

        self.copy_button_1 = tk.Button(self, image=copy_btn_image, borderwidth=0,
                                       command=lambda: logic.copy_password(0, passwords))
        self.copy_button_2 = tk.Button(self, image=copy_btn_image, borderwidth=0,
                                       command=lambda: logic.copy_password(1, passwords))
        self.copy_button_3 = tk.Button(self, image=copy_btn_image, borderwidth=0,
                                       command=lambda: logic.copy_password(2, passwords))
        self.copy_button_4 = tk.Button(self, image=copy_btn_image, borderwidth=0,
                                       command=lambda: logic.copy_password(3, passwords))
        self.copy_buttons = [self.copy_button_1, self.copy_button_2,
                             self.copy_button_3, self.copy_button_4]

        self.frame_title = tk.Label(self, text='Generate password', font=title_font)
        self.frame_title.grid(column=0, row=0, columnspan=4)

        self.question = tk.Label(self, text='Number of characters (4 to 100):', font=description_font)
        self.question.grid(column=0, row=1, columnspan=4)

        self.character_sets_label = tk.Label(self, text='Character sets', font=section_title_font)
        self.character_sets_label.grid(column=5, row=3, columnspan=2, sticky='s')

        self.lowercase_letters_var = tk.IntVar()
        self.lowercase_letters_checkbox = tk.Checkbutton(self, variable=self.lowercase_letters_var,
                                                         offvalue=0, onvalue=1)
        self.lowercase_letters_text = tk.Label(self, text='Lowercase letters', font=description_font)

        self.uppercase_letters_var = tk.IntVar()
        self.uppercase_letters_checkbox = tk.Checkbutton(self, variable=self.uppercase_letters_var,
                                                         offvalue=0, onvalue=1)
        self.uppercase_letters_text = tk.Label(self, text='Uppercase letters', font=description_font)

        self.digits_var = tk.IntVar()
        self.digits_checkbox = tk.Checkbutton(self, variable=self.digits_var,
                                              offvalue=0, onvalue=1)
        self.digits_text = tk.Label(self, text='Digits', font=description_font)

        self.punctuation_var = tk.IntVar()
        self.punctuation_checkbox = tk.Checkbutton(self, variable=self.punctuation_var,
                                                   offvalue=0, onvalue=1)
        self.punctuation_text = tk.Label(self, text='Punctuation', font=description_font)

        self.checkboxes = [self.lowercase_letters_checkbox, self. uppercase_letters_checkbox,
                           self.digits_checkbox, self.punctuation_checkbox]
        self.checkboxes_text_labels = [self.lowercase_letters_text, self.uppercase_letters_text,
                                       self.digits_text, self.punctuation_text]

        self.other_methods_window = None

        self.try_other_methods_btn = tk.Button(self, image=try_other_methods_btn_image,
                                               borderwidth=0,
                                               command=self.open_other_methods)
        self.try_other_methods_btn.grid(row=0, column=2, rowspan=3, columnspan=6)

        for checkbox in self.checkboxes:
            checkbox.grid(column=5, row=4 + self.checkboxes.index(checkbox), pady=8)
            checkbox.select()

        for text_label in self.checkboxes_text_labels:
            text_label.grid(column=6, row=4 + self.checkboxes_text_labels.index(text_label), sticky='w')

        def create_password_labels() -> None:
            """
            Called upon clicking the done button or pressing the ENTER key,
            this function calls determine_error and validate_character_sets of generate_password_logic,
            and then settles whether an error has occurred or not.
            If an error has occurred, the function displays said error
            (obtained through determine_error),
            and displays it on the screen through show_text.
            If an error has not occurred,
            the function calls generate_password of generate_password_logic.py to get 4 passwords,
            and calls the show_text function to display them to the user.
            """
            global passwords

            for password_label in self.password_labels:
                password_label.bind('<Button-3>', lambda e: logic.show_copy_button(e, copy_menu))

            message = logic.determine_error(
                logic.validate_character_sets(self.lowercase_letters_var, self.uppercase_letters_var,
                                              self.digits_var, self.punctuation_var),
                input_box.get(), no_character_set_error, double_error, invalid_input_error)

            # Check if an error was not returned
            if message == '':
                passwords = []
                for password_label in self.password_labels:
                    password_label.grid(column=0, row=4 + self.password_labels.index(password_label), pady=10, padx=10)
                    adapted_input = logic.adapt_input(input_box.get())
                    input_box.delete(0, 'end')
                    input_box.insert(1, str(adapted_input))

                    message = logic.generate_password(adapted_input, self.lowercase_letters_var,
                                                      self.uppercase_letters_var, self.digits_var, self.punctuation_var)
                    passwords.append(message)

                    show_text(password_label, '')
                    password_label.grid(column=0, row=4 + self.password_labels.index(password_label), pady=10, padx=10)
                for index, button in enumerate(self.show_hide_buttons):
                    button.grid(row=4 + index, column=1, columnspan=2, padx=15)
                for index, copy_button in enumerate(self.copy_buttons):
                    copy_button.grid(row=4 + index, column=3, columnspan=2, padx=15)
                self.show_hide_all_slider.grid(row=3, column=2, columnspan=2)
                self.hide_label.grid(row=3, column=1, sticky='w')
                self.show_label.grid(row=3, column=4, sticky='e')

            else:
                messagebox.showerror('Error', message)
                if message == invalid_input_error or message == double_error:
                    input_box.delete(0, 'end')

            hide_all_passwords()
            for button in self.show_hide_buttons:
                hide_password(self.show_hide_buttons.index(button), button)

        global input_box
        input_box = tk.Entry(self, width=10, borderwidth=2)
        input_box.bind('<Return>', lambda e: create_password_labels())
        input_box.grid(column=0, row=2, columnspan=4)

        self.done_btn = tk.Button(self, image=done_btn_image, borderwidth=0, command=lambda: create_password_labels())
        self.done_btn.grid(column=0, row=3, columnspan=4)

        global copy_menu
        copy_menu = tk.Menu(self, tearoff=False)
        copy_menu.add_command(label='Copy', command=lambda: logic.copy_selected_text(input_box, password_labels))

        def show_text(label, message) -> None:
            """
            Called by the create_password_labels function,
            this function updates the contents of the password_labels,
            by enabling the label, deleting its current contents,
            inserting the new text, and then disabling the label again.

            Parameters
            ----------
            label: tkinter.Text
                Each password label one by one if passwords are generated,
                or the first password label if an error is generated.
            message: str
                Each password or the error.
            """
            label.config(state='normal')
            label.delete('1.0', 'end')
            label.insert('1.0', message)
            label.config(state='disabled', bg='#ffffff')

    def open_other_methods(self):
        """
        Called when the user clicks on the 'try other methods' button,
        this function creates a Toplevel window containing other methods of password generation.
        """
        print('Hello, world!')
        if self.other_methods_window is None or not self.other_methods_window.winfo_exists():
            self.other_methods_window = other.OtherMethodsWindow(self)
        else:
            self.other_methods_window.focus()


def select_input_box() -> None:
    """
    Called whenever the tab is changed,
    this function focuses the keyboard to the input box,
    which allows the user to start typing immediately without having to click on the input box first.
    """
    input_box.focus()
