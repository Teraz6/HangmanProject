# Hangman game with tkinter

import random
import tkinter as tk
from tkinter import ttk   #imports tk themed widgets
from tkinter import messagebox


class HangmanApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Hangman")# Window title
        self.geometry("800x600")# Defines window size
        self.minsize(600, 400)
        self.maxsize(1000, 600)
        self.iconbitmap("./Images/Icon.ico")# window icon img

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, GamePage, EndPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



        # Custom style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), background="#242424", foreground="black", padding=10)

        label = ttk.Style()
        label.configure("TLabel",font=("Arial", 14), background="#8a8a8a", foreground="black")

        #Label
        message = ttk.Label(self, text="Welcome to Hangman!", style="TLabel", font=("Arial", 20))
        message.pack(pady=20)

        #Buttons
        lvl1 = ttk.Button(self, text="Easy", style="TButton", command=lambda: controller.show_frame(GamePage))
        lvl1.pack(side="top", pady=10)

        lvl2 = ttk.Button(self, text="Medium", style="TButton", command=lambda: controller.show_frame(GamePage))
        lvl2.pack(side="top", pady=10)

        lvl3 = ttk.Button(self, text="Hard", style="TButton", command=lambda: controller.show_frame(GamePage))
        lvl3.pack(side="top", pady=10)

        lvl4 = ttk.Button(self, text="Extreme", style="TButton", command=lambda: controller.show_frame(GamePage))
        lvl4.pack(side="top", pady=10)

        exit_button = ttk.Button(self, text="Exit", style="TButton", command=lambda: controller.destroy())
        exit_button.pack(side="right",padx=10)


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        guess_entry = ttk.Entry(self, width=20, font=("Arial", 18))
        guess_entry.pack(side="bottom", padx=10, pady=20)
        guess_button = ttk.Button(self, text="Guess")
        guess_button.pack(side="bottom", anchor="se", padx=10)



class EndPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



# Run the app
if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()