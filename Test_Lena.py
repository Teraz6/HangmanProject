import random
import tkinter as tk
from tkinter import ttk, messagebox

# Mängu loogika klass (jätka sama)
class HangmanGame:
    def __init__(self):
        self.lives = 6
        self.chosen_word = ""
        self.correct_letters = set()
        self.guessed_letters = set()

    def start_game(self, filename):
        try:
            with open(filename, "r") as file:
                word_list = [word.strip() for word in file.read().split(",") if word.strip()]
                self.chosen_word = random.choice(word_list).lower()
                self.lives = 6
                self.correct_letters.clear()
                self.guessed_letters.clear()
                return True
        except FileNotFoundError:
            messagebox.showerror("Viga", f"Faili '{filename}' ei leitud!")
            return False

    def guess_letter(self, letter):
        if not self.chosen_word or self.lives == 0:
            return False  # Mäng on lõppenud

        letter = letter.lower()

        if letter in self.guessed_letters:
            messagebox.showinfo("Korduv täht", f"Oled juba pakkunud '{letter}'")
            return False

        self.guessed_letters.add(letter)

        if letter in self.chosen_word:
            self.correct_letters.add(letter)
            return True
        else:
            self.lives -= 1
            return False

    def get_display_word(self):
        return "".join([c if c in self.correct_letters else "_" for c in self.chosen_word])

    def is_won(self):
        return all(char in self.correct_letters for char in self.chosen_word)

    def is_lost(self):
        return self.lives == 0

    def get_lives(self):
        return self.lives

    def get_chosen_word(self):
        return self.chosen_word

# Mängu visuaalne klass (kasuta seda versiooni)
class HangmanDisplay:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self.canvas = tk.Canvas(master, width=300, height=300, bg="white")
        self.canvas.place(x=550, y=80)
        self.word_display = ttk.Label(master, text="", font=("Courier", 24))
        self.word_display.place(x=550, y=20)
        self.message_label = ttk.Label(master, text="Alusta mängu!", font=("Arial", 16))
        self.message_label.place(x=550, y=320)
        self.hangman_images = []
        for i in range(7):
            try:
                img = tk.PhotoImage(file=f"./Images/TikiMan1HB{i + 1}.png")
                self.hangman_images.append(img)
                print(f"Pilt TikiMan1HB{i + 1}.png laaditi edukalt.")
            except tk.TclError as e:
                messagebox.showerror("Viga pildi laadimisel", f"Ei saanud laadida pilti TikiMan1HB{i + 1}.png: {e}")
                self.hangman_images.append(None)  # Lisa None, et listi pikkus oleks õige

        print(f"Piltide laadimine tulemus: {self.hangman_images}")

        # Loome pildi canvas'ile alles pärast canvas'i loomist
        if self.hangman_images[0]:
            self.hangman_image_on_canvas = self.canvas.create_image(150, 150, image=self.hangman_images[0])
        else:
            self.hangman_image_on_canvas = None

        self.guessed_letters_label = ttk.Label(master, text="Pakutud tähed:", font=("Arial", 12))
        self.guessed_letters_label.place(x=700, y=80)
        self.guessed_letters_display = ttk.Label(master, text="", font=("Courier", 14))
        self.guessed_letters_display.place(x=700, y=100)
        self.update_hangman_image()

    def update_word(self):
        self.word_display.config(text=f"Sõna: {self.game.get_display_word()}")

    def update_lives(self):
        self.message_label.config(text=f"Elud: {self.game.get_lives()}")
        self.update_hangman_image()

    def show_win_message(self):
        self.message_label.config(text=f"Võitsid! Sõna oli: {self.game.get_chosen_word()}")

    def show_lose_message(self):
        self.message_label.config(text=f"Kaotasid! Sõna oli: {self.game.get_chosen_word()}")

    def update_hangman_image(self):
        lives_left = self.game.get_lives()
        index = 6 - lives_left
        print(f"Uuendatakse pilti. Elud: {lives_left}, indeks: {index}")
        if 0 <= index < len(self.hangman_images):
            if self.hangman_image_on_canvas:
                print(f"Uuendatakse pilti indeksiga {index}")
                self.canvas.itemconfig(self.hangman_image_on_canvas, image=self.hangman_images[index])
            else:
                print("Canvas element pildi jaoks pole veel loodud!")
        else:
            print(f"Vigane pildi indeks: {index}")

    def update_guessed_letters(self):
        self.guessed_letters_display.config(text=", ".join(sorted(list(self.game.guessed_letters))))

# Peamine rakenduse klass
class HangmanApp:
    def __init__(self, master):
        self.master = master
        master.title("Hangman Project")
        master.geometry("1000x600")
        master.resizable(False, False)
        try:
            master.iconbitmap("./Images/icon.ico")
        except tk.TclError:
            pass # Ikoni laadimine ei ole kriitiline

        self.game = HangmanGame()
        self.display = HangmanDisplay(master, self.game) # Loome HangmanDisplay objekti

        self.message_label_top = ttk.Label(master, text="Vali raskusaste", font=("Arial", 14))
        self.message_label_top.place(x=40, rely=0.1)

        ttk.Button(master, text="Easy", command=lambda: self.start_new_game("words_easy.txt")).place(x=40, rely=0.2, width=130, height=40)
        ttk.Button(master, text="Medium", command=lambda: self.start_new_game("words_medium.txt")).place(x=40, rely=0.3, width=130, height=40)
        ttk.Button(master, text="Hard", command=lambda: self.start_new_game("words_hard.txt")).place(x=40, rely=0.4, width=130, height=40)
        ttk.Button(master, text="Extreme", command=lambda: self.start_new_game("words_extreme.txt")).place(x=40, rely=0.5, width=130, height=40)
        ttk.Button(master, text="All words", command=lambda: self.start_new_game("words_all.txt")).place(x=40, rely=0.6, width=130, height=40)

        ttk.Button(master, text="Välju mängust", command=master.destroy).place(x=40, rely=0.9, width=150, height=50)

        self.guess_entry = ttk.Entry(master, font=("Arial", 18))
        self.guess_entry.place(relx=0.6, rely=0.8, width=200, height=50)

        self.guess_button = ttk.Button(master, text="Paku", command=self.on_guess)
        self.guess_button.place(relx=0.85, rely=0.8, width=70, height=50)

        master.bind('<Return>', lambda event: self.on_guess()) # Võimaldab Enter-klahviga pakkuda

    def start_new_game(self, filename):
        print(f"Alustatakse uut mängu failiga: {filename}")
        if self.game.start_game(filename):
            self.display.update_word()
            self.display.update_lives()
            self.display.update_guessed_letters()
            self.guess_entry.config(state=tk.NORMAL)
            self.guess_entry.delete(0, tk.END)
            self.display.message_label.config(text="Mäng algas! Paku tähte.")

    def on_guess(self):
        letter = self.guess_entry.get()
        self.guess_entry.delete(0, tk.END)
        if letter:
            print(f"Pakutud täht: {letter}")
            was_correct = self.game.guess_letter(letter[0])
            if was_correct:
                print("Täht oli õige.")
                self.display.update_word()
                self.display.update_guessed_letters()
                if self.game.is_won():
                    self.display.show_win_message()
                    self.guess_entry.config(state=tk.DISABLED)
            else:
                print("Täht oli vale.")
                self.display.update_lives()
                self.display.update_guessed_letters()
                if self.game.is_lost():
                    self.display.show_lose_message()
                    self.guess_entry.config(state=tk.DISABLED)

if __name__ == "__main__":
    window = tk.Tk()
    app = HangmanApp(window) # Loome HangmanApp objekti
    window.mainloop()