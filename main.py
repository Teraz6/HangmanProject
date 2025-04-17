# Hangman game with tkinter

import random
import tkinter as tk
from tkinter import ttk   #imports tk themed widgets
from tkinter import messagebox

window = tk.Tk()

# Window title
window.title("Hangman Project")

# Defines window size
window.geometry("1000x600")
window.resizable(False, False)  #Window size can´t be changed

# This is for limiting window size, when window resizing is allowed
    #window.minsize(800, 600)
    #window.maxsize(1000, 800)

# window icon img
window.iconbitmap("./images/icon.ico")

# Display the message when starting.
message = ttk.Label(window, text="Welcome to Hangman!", font=("Arial", 20))
message.pack()

# Changes style on ALL buttons
s = ttk.Style()
s.configure("TButton", background="#d2d2d4", foreground="Black", font=("Arial", 14))

# Start game function
def start_game(filename):
    with open(filename, "r") as file:
        content = file.read()  # Puts all words into single string. example: apple,banana,cherry
        word_list = [word.strip() for word in content.split(",") if word.strip()]  # Splits string by "," and puts into list ["apple", "banana", "cherry"]
        random_word = random.choice(word_list)  # Chooses one random word from the list
    return random_word

    #TODO: code that hides the word and displays underscores for every letter


# Text above difficulty buttons
difficulty_text = ttk.Label(window, text="Choose difficulty", font=("Arial", 16))
difficulty_text.place(relx=0.42, rely=0.1)


# Choose difficulty buttons
# NB! start_game("word.txt") starts the function. With this there isn´t need for start game button
lvl1 = ttk.Button(window, text="Easy", command= lambda: start_game("words_easy.txt"))
lvl1.place(x=435, rely=0.2, width=130, height=40)
lvl2 = ttk.Button(window, text="Medium", command= lambda: start_game("words_medium.txt"))
lvl2.place(x=435, rely=0.3, width=130, height=40)
lvl3 = ttk.Button(window, text="Hard", command= lambda: start_game("words_hard.txt"))
lvl3.place(x=435, rely=0.4, width=130, height=40)
lvl4 = ttk.Button(window, text="Extreme", command= lambda: start_game("words_extreme.txt"))
lvl4.place(x=435, rely=0.5, width=130, height=40)
# TODO add button and func for words_all.txt file?

# Close game button
exit_button = ttk.Button(window, text="Exit game", command=window.destroy)
exit_button.place(x=425, rely=0.9, width=150, height=50)


# TODO: display guessed letters
# TODO: display word that is being guessed

# Displays window
window.mainloop()



