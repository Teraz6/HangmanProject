import Display

class HangmanApp:
    def __init__(self, master):
        # ... olemasolev kood ...
        self.display = Display(master, self.game)
        # ... ülejäänud kood ...

    def on_guess(self, tk=None):
        letter = self.guess_entry.get()
        self.guess_entry.delete(0, tk.END)
        if letter:
            if self.game.guess_letter(letter[0]):
                self.display.update_word()
                self.display.update_guessed_letters(self.game.guessed_letters) # Uuendame kuvatavaid tähti
                if self.game.is_won():
                    self.display.show_win_message()
                    self.guess_entry.config(state=tk.DISABLED)
            else:
                self.display.update_lives()
                self.display.update_guessed_letters(self.game.guessed_letters) # Uuendame kuvatavaid tähti ka vale pakkumise korral
                if self.game.is_lost():
                    self.display.show_lose_message()
                    self.guess_entry.config(state=tk.DISABLED)

