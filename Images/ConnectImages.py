def start_game(filename):
    global random_word, guessed_letters, wrong_guesses
    with open(filename, "r") as file:
        content = file.read()
        word_list = [word.strip() for word in content.split(",") if word.strip()]
        random_word = random.choice(word_list).lower()
    guessed_letters = set()
    wrong_guesses = 0
    update_displayed_word()
    update_hangman_image()
    message.config(text="Game started! Guess a letter.")

hangman_images = [tk.PhotoImage(file=f"./images/hangman{i}.png") for i in range(7)] #Alla laetu filedega

def update_hangman_image():
    game_display.itemconfig(hangman_image_on_canvas, image=hangman_images[wrong_guesses])

word_label = ttk.Label(window, text="", font=("Courier", 24))
word_label.place(relx=0.5, rely=0.7, anchor="center")

def guess_letter():
    global wrong_guesses
    letter = guess_entry.get().lower()
    guess_entry.delete(0, tk.END)

    if not letter.isalpha() or len(letter) != 1:
        message.config(text="Please enter one letter.")
        return

    if letter in guessed_letters:
        message.config(text="You already guessed that letter.")
        return

    guessed_letters.add(letter)

    if letter in random_word:
        update_displayed_word()
        if "_" not in word_label.cget("text"):
            message.config(text=f"You won! The word was: {random_word}")
    else:
        wrong_guesses += 1
        update_hangman_image()
        if wrong_guesses == 6:
            message.config(text=f"You lost! The word was: {random_word}")
            word_label.config(text=random_word)

guess_button.config(command=guess_letter)

