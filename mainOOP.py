import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from PIL import Image, ImageTk, ImageDraw, ImageFont


class HangmanApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Hangman")
        self.geometry("800x600")
        self.minsize(600, 400)
        self.maxsize(1000, 600)
        self.iconbitmap("./Images/Icon.ico")  # Optional icon path

        self.word_list = None

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

    def show_frame(self, cont, word_list=None):
        frame = self.frames[cont]
        if isinstance(frame, GamePage) and word_list:
            frame.word_list = word_list
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

    def start_game(self, filename):
        with open(filename, "r") as f:
            line = f.readline()
            self.word_list = [word.strip().lower() for word in line.split(",") if word.strip()]
        self.show_frame(GamePage, self.word_list)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=10)
        label = ttk.Style()
        label.configure("TLabel", font=("Arial", 14), foreground="black")

        message = ttk.Label(self, text="Welcome to Hangman!", style="TLabel", font=("Arial", 20))
        message.pack(pady=20)

        lvl1 = ttk.Button(self, text="Easy", style="TButton",
                          command=lambda: self.start_game("words_easy.txt"))
        lvl1.pack(side="top", pady=10)

        lvl2 = ttk.Button(self, text="Medium", style="TButton",
                          command=lambda: self.start_game("words_medium.txt"))
        lvl2.pack(side="top", pady=10)

        lvl3 = ttk.Button(self, text="Hard", style="TButton",
                          command=lambda: self.start_game("words_hard.txt"))
        lvl3.pack(side="top", pady=10)

        lvl4 = ttk.Button(self, text="Extreme", style="TButton",
                          command=lambda: self.start_game("words_extreme.txt"))
        lvl4.pack(side="top", pady=10)

        exit_button = ttk.Button(self, text="Exit", style="TButton", command=controller.destroy)
        exit_button.pack(side="right", padx=10)

    def start_game(self, filename):
        word_list = self.load_words_from_file(filename)
        if word_list:
            self.controller.show_frame(GamePage, word_list)

    def load_words_from_file(self, filename):
        with open(filename, "r") as file:
            return [word.strip().lower() for word in file.readline().split(",")]


class GamePage(tk.Frame):
    def __init__(self, parent, controller, word_list=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.word_list = word_list or []
        self.chosen_word = ""
        self.previous_guesses = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6

        self.word_label = ttk.Label(self, text="", font=("Arial", 20))
        self.word_label.pack(side="top", pady=20, anchor="center")

        self.remaining_label = ttk.Label(self,
                                         text=f"Remaining attempts: {self.max_wrong_guesses}",
                                         font=("Arial", 14))
        self.remaining_label.pack(side="top")

        self.canvas = tk.Canvas(self, width=300, height=300)
        self.canvas.pack(pady=10)
        self.hangman_image = None
        self.update_hangman_image()  # Kuvab esialgse pildi mängu alguses

        def validate_input(p):
            return p == "" or (len(p) == 1 and p.isalpha())

        validate_command = (self.register(validate_input), "%P")

        self.guess_entry = ttk.Entry(self, width=20, font=("Arial", 18),
                                     validate="key", validatecommand=validate_command)
        self.guess_entry.pack(side="bottom", padx=10, pady=10)

        self.guess_display = ttk.Label(self, text="", font=("Arial", 18))
        self.guess_display.pack(side="bottom", anchor="sw", padx=10, pady=10)

        self.guess_info_display = ttk.Label(self, text="Guessed letters", font=("Arial", 14))
        self.guess_info_display.pack(side="bottom", anchor="sw", padx=10, pady=10)

        guess_button = ttk.Button(self, text="Guess", command=self.display_guess)
        guess_button.pack(side="bottom", anchor="se", padx=10)

        self.bind("<<ShowFrame>>", self.on_show_frame)

    def update_hangman_image(self): # pildi meetod
        self.canvas.delete("all")
        try:
            if self.wrong_guesses == 0:
                img = Image.open("./Images/TikiMan0.png")
            elif self.wrong_guesses == 1:
                img = Image.open("./Images/TikiMan1.png")
            elif self.wrong_guesses == 2:
                img = Image.open("./Images/TikiMan2.png")
            elif self.wrong_guesses == 3:
                img = Image.open("./Images/TikiMan3.png")
            elif self.wrong_guesses == 4:
                img = Image.open("./Images/TikiMan4.png")
            elif self.wrong_guesses == 5:
                img = Image.open("./Images/TikiMan5.png")
            elif self.wrong_guesses >= 6:
                img = Image.open("./Images/TikiMan6.png")
            else:
                img = None

            if img:
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                self.hangman_image = ImageTk.PhotoImage(img)
                self.canvas.create_image(150, 150, image=self.hangman_image)

        except FileNotFoundError as e:
            print(f"Viga: Pildifaili ei leitud! {e}")
        except Exception as e:
            print(f"Viga pildi laadimisel: {e}")

    def on_show_frame(self, event):
        if self.word_list:
            self.chosen_word = random.choice(self.word_list).lower()
        else:
            self.chosen_word = "default"

        self.previous_guesses = []
        self.wrong_guesses = 0
        self.update_displayed_word()
        self.update_remaining_attempts()

        self.guess_display.config(text="")
        self.guess_entry.delete(0, tk.END)

    def display_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if not guess:
            return

        if guess in self.previous_guesses:
            messagebox.showinfo("Oops", "You already guessed that letter.")
            return

        self.previous_guesses.append(guess)

        if guess not in self.chosen_word:
            self.wrong_guesses += 1
            self.update_hangman_image()  # uuendab pildi iga vale vastusega

        self.update_displayed_word()
        self.update_remaining_attempts()

        self.guess_display.config(text=" ".join(self.previous_guesses))

        if all(letter in self.previous_guesses for letter in set(self.chosen_word)):
            self.controller.frames[EndPage].set_result(True, self.chosen_word)
            self.controller.show_frame(EndPage)
            return

        if self.wrong_guesses >= self.max_wrong_guesses:
            self.controller.frames[EndPage].set_result(False, self.chosen_word)
            self.controller.show_frame(EndPage)
            return

    def update_displayed_word(self):
        displayed = " ".join([
            letter if letter in self.previous_guesses else "_"
            for letter in self.chosen_word
        ])
        self.word_label.config(text=displayed)

    def update_remaining_attempts(self):
        remaining = self.max_wrong_guesses - self.wrong_guesses
        self.remaining_label.config(text=f"Remaining attempts: {remaining}")


class EndPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.message_label = ttk.Label(self, text="", font=("Arial", 24))
        self.message_label.pack(pady=30)

        self.word_label = ttk.Label(self, text="", font=("Arial", 18))
        self.word_label.pack(pady=10)

        play_again = ttk.Button(self, text="Play Again", command=lambda: controller.show_frame(StartPage))
        play_again.pack(pady=10)

        exit_btn = ttk.Button(self, text="Exit", command=controller.destroy)
        exit_btn.pack(pady=10)

    def set_result(self, won, word):
        if won:
            self.message_label.config(text="🎉 You Won! 🎉", foreground="green")
            self.word_label.config(text="")
        else:
            self.message_label.config(text="💀 You Lost!", foreground="red")
            self.word_label.config(text=f"The word was: {word}")


# Run the app
if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()
