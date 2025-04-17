import random

lives = 6

# Küsi kasutajalt raskusastet
difficulty = input("Vali raskusaste (easy / medium / hard / extreme / all): ").lower()

# Faili nimi vastavalt valikule
filename = f"words_{difficulty}.txt"

try:
    with open(filename) as file:
        word_list = file.read().split(', ')
except FileNotFoundError:
    print("Faili ei leitud või vale raskusaste. Kasutan vaikimisi 'easy'.")
    with open("words_easy.txt") as file:
        word_list = file.read().split(', ')

chosen_word = random.choice(word_list)

placeholder = ""
word_length = len(chosen_word)
for position in range(word_length):
    placeholder += "_"
print("Word to guess: " + placeholder)

game_over = False
correct_letters = []

while not game_over:

    print(f"****************************{lives}/6 LIVES LEFT****************************")
    guess = input("Guess a letter: ").lower()

    if guess in correct_letters:
        print(f"You've already guessed {guess}")

    display = ""

    for letter in chosen_word:
        if letter == guess:
            display += letter
            correct_letters.append(guess)
        elif letter in correct_letters:
            display += letter
        else:
            display += "_"

    print("Word to guess: " + display)

    if guess not in chosen_word:
        lives -= 1
        print(f"You guessed {guess}, that's not in the word. You lose a life.")

        if lives == 0:
            game_over = True

            print(f"***********************IT WAS {chosen_word}! YOU LOSE**********************")

    if "_" not in display:
        game_over = True
        print("****************************YOU WIN****************************")

    print([lives])
