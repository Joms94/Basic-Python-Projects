import random


class Dictionary:
    def __init__(self):
        pass

    def generate_word(self):
        # This generates and returns a random word from the dictionary.
        return "WORD"
        ...


class DevilsDictionary(Dictionary):
    def generate_word(self):
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        length = random.randint(5, 10)
        magic_words = ''.join((random.choice(letters) for i in range(length)))
        return magic_words
