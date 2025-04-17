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
        self.hangman_images = [tk.PhotoImage(file=f"./Images/TikiMan1HB{i+1}.png") for i in range(7)]
        self.hangman_image_on_canvas = self.canvas.create_image(150, 150, image=self.hangman_images[0])
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
        if 0 <= index < len(self.hangman_images):
            self.canvas.itemconfig(self.hangman_image_on_canvas, image=self.hangman_images[index])

    def update_guessed_letters(self, guessed_letters):
        self.guessed_letters_display.config(text=", ".join(sorted(list(guessed_letters))))