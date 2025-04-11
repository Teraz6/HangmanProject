import random

"""
This file is for testing purpose and is excluding tkinter for easier understanding, how code is working
"""

def start_game(filename):
    with open(filename, "r") as file:
        content = file.read()  # Puts all words into single string. example: apple,banana,cherry
        word_list = [word.strip() for word in content.split(",") if word.strip()]  # Splits string by "," and puts into list ["apple", "banana", "cherry"]
        random_word = random.choice(word_list)  # Chooses one random word from the list
        #return random_word   Probably not needed
        letter_count_in_random_word = len(random_word)  #Counts how many letters in random_word
        hide_words = ["_"] * letter_count_in_random_word  #Hides the word by adding "_" into the list
        print(hide_words, random_word) # For testing purpose atm. 
        guess_letter = input("Guess the letter: ")
        guess_word = list(random_word)  # Word that is being guessed
        if guess_letter in guess_word: # TODO: FOR loop to be able to guess entire word
            letter_position = guess_word.index(guess_letter)   # Finds letter position in the word
            hide_words[letter_position] = guess_letter   #Places letter in the list to correct position
            print(hide_words)
            print("Correct!")
        else:
            print("Incorrect!")

if __name__ == '__main__':
    start_game("words_easy.txt")