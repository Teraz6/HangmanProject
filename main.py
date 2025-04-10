# Hangman game with tkinter

import random
import tkinter as tk
from tkinter import ttk   #imports tk themed widgets

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
s.configure("TButton", background="#000000", foreground="#0307ff", font=("Arial", 14))

# Start game function
def start_game(filename):
    #TODO code for .txt file reading
    print("Game started!")

# Start game button
start_game_button = ttk.Button(window, text="Start Game", command="start_game")
start_game_button.pack(ipadx=10, ipady=10, expand=False)
start_game_button.place(x=40, rely=0.1, width=150, height=50)  # Button placement and size

# Text above difficulty buttons
difficulty_text = ttk.Label(window, text="Choose difficulty", font=("Arial", 14))
difficulty_text.pack()
difficulty_text.place(x=40, rely=0.3)


# Choose difficulty buttons
# NB! start_game("word.txt") starts the function. With this there isn´t need for start game button
lvl1 = ttk.Button(window, text="Level 1", command= lambda: start_game("words_easy.txt"))
lvl1.pack(ipadx=10, ipady=10, expand=False)
lvl1.place(x=40, rely=0.4, width=130, height=40)
lvl2 = ttk.Button(window, text="Level 2", command= lambda: start_game("words_medium.txt"))
lvl2.pack(ipadx=10, ipady=10, expand=False)
lvl2.place(x=40, rely=0.5, width=130, height=40)
lvl3 = ttk.Button(window, text="Level 3", command= lambda: start_game("words_hard.txt"))
lvl3.pack(ipadx=10, ipady=10, expand=False)
lvl3.place(x=40, rely=0.6, width=130, height=40)
lvl4 = ttk.Button(window, text="Level 4", command= lambda: start_game("words_extreme.txt"))
lvl4.pack(ipadx=10, ipady=10, expand=False)
lvl4.place(x=40, rely=0.7, width=130, height=40)
# TODO add button and func for words_all.txt file

# Close game button
exit_button = ttk.Button(window, text="Exit game", command=window.destroy)
exit_button.pack(ipadx=10, ipady=10, expand=False)
exit_button.place(x=40, rely=0.9, width=150, height=50)

#Guess entry and button
guess_entry = ttk.Entry(window)
guess_entry.place(relx=0.6, rely=0.8, width=200, height=50)
guess_button = ttk.Button(window, text="Guess")
guess_button.place(relx=0.85, rely=0.8, width=70, height=50)

# Canvas for game display
game_display = tk.Canvas(window, width=400, height=400, bg="white")
game_display.pack(expand=False)
game_display.place(x=550, y=50)

# TODO: display guessed letters
# TODO: display word that is being guessed

# Displays window
window.mainloop()



