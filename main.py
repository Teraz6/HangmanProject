#GERVINI BASE_GAME JA MAINI-BRANCHIST VÕETUD MÄNGU KOODI KOMBO
#TÖÖTAB

import random
import tkinter as tk
from tkinter import ttk, messagebox

# Mängu põhiloogika klass
class HangmanGame:
    def __init__(self, canvas, display_label):
        self.canvas = canvas
        self.display_label = display_label
        self.lives = 6
        self.chosen_word = ""
        self.correct_letters = set()
        self.guessed_letters = set()

    def start_game(self, filename):
        try:
            with open(filename, "r") as file:
                word_list = [word.strip() for word in file.read().split(",") if word.strip()]
                self.chosen_word = random.choice(word_list)
                self.lives = 6
                self.correct_letters.clear()
                self.guessed_letters.clear()
                self.update_display()
                self.canvas.delete("all")
        except FileNotFoundError:
            messagebox.showerror("Viga", f"Faili '{filename}' ei leitud!")

    def guess_letter(self, letter):
        if not self.chosen_word or self.lives == 0:
            return

        letter = letter.lower()

        if letter in self.guessed_letters:
            messagebox.showinfo("Korduv täht", f"Oled juba pakkunud '{letter}'")
            return

        self.guessed_letters.add(letter)

        if letter in self.chosen_word:
            self.correct_letters.add(letter)
        else:
            self.lives -= 1
            self.draw_hangman()

        self.update_display()

        if self.lives == 0:
            self.display_label.config(text=f"Sõna oli: {self.chosen_word}. Kaotasid!")
        elif all(char in self.correct_letters for char in self.chosen_word):
            self.display_label.config(text=f"Võitsid! Sõna oli: {self.chosen_word}")

    def update_display(self):
        display_word = "".join([c if c in self.correct_letters else "_" for c in self.chosen_word])
        self.display_label.config(text=f"Sõna: {display_word}\nElud: {self.lives}")

    def draw_hangman(self):
        parts = [
            lambda: self.canvas.create_oval(170, 50, 210, 90),             # pea
            lambda: self.canvas.create_line(190, 90, 190, 160),            # keha
            lambda: self.canvas.create_line(190, 110, 160, 140),           # vasak käsi
            lambda: self.canvas.create_line(190, 110, 220, 140),           # parem käsi
            lambda: self.canvas.create_line(190, 160, 160, 200),           # vasak jalg
            lambda: self.canvas.create_line(190, 160, 220, 200),           # parem jalg
        ]
        index = 6 - self.lives - 1
        if 0 <= index < len(parts):
            parts[index]()

# Tkinter GUI
window = tk.Tk()
window.title("Hangman Project")
window.geometry("1000x600")
window.resizable(False, False)
window.iconbitmap("./images/icon.ico")

message = ttk.Label(window, text="Tere tulemast mängu!", font=("Arial", 20))
message.pack()

s = ttk.Style()
s.configure("TButton", font=("Arial", 14))

word_display = ttk.Label(window, text="", font=("Courier", 24))
word_display.place(x=550, y=20)

canvas = tk.Canvas(window, width=300, height=300, bg="white")
canvas.place(x=550, y=80)

game = HangmanGame(canvas, word_display)

difficulty_text = ttk.Label(window, text="Vali raskusaste", font=("Arial", 14))
difficulty_text.place(x=40, rely=0.1)

ttk.Button(window, text="Easy", command=lambda: game.start_game("words_easy.txt")).place(x=40, rely=0.2, width=130, height=40)
ttk.Button(window, text="Medium", command=lambda: game.start_game("words_medium.txt")).place(x=40, rely=0.3, width=130, height=40)
ttk.Button(window, text="Hard", command=lambda: game.start_game("words_hard.txt")).place(x=40, rely=0.4, width=130, height=40)
ttk.Button(window, text="Extreme", command=lambda: game.start_game("words_extreme.txt")).place(x=40, rely=0.5, width=130, height=40)
ttk.Button(window, text="All words", command=lambda: game.start_game("words_all.txt")).place(x=40, rely=0.6, width=130, height=40)

exit_button = ttk.Button(window, text="Välju mängust", command=window.destroy)
exit_button.place(x=40, rely=0.9, width=150, height=50)

guess_entry = ttk.Entry(window, font=("Arial", 18))
guess_entry.place(relx=0.6, rely=0.8, width=200, height=50)

def on_guess():
    letter = guess_entry.get()
    if letter:
        game.guess_letter(letter[0])
        guess_entry.delete(0, tk.END)

guess_button = ttk.Button(window, text="Paku", command=on_guess)
guess_button.place(relx=0.85, rely=0.8, width=70, height=50)

window.mainloop()
