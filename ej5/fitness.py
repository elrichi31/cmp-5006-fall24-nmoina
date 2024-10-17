import math
import json
import random
import time

class AlphabetInvalid(Exception):
    """Exception raised for invalid alphabets"""
    pass

class Key:
    """Class representing the substitution key for breaking the cipher"""

    @staticmethod
    def check_alphabet(alphabet):
        """Ensure the alphabet is valid (no more than 32 characters)"""
        if len(alphabet) > 32:
            raise AlphabetInvalid("Alphabet must have less than or equal to 32 characters")
        return alphabet

    def __init__(self, key, alphabet):
        self.key = key
        self.alphabet = alphabet
        self._key_map = {ch: self.key[idx] for idx, ch in enumerate(self.alphabet)}

    def decode(self, ciphertext):
        """Decode the ciphertext using the substitution key"""
        return ''.join([self._key_map[ch] for ch in ciphertext.lower() if ch in self._key_map])

class BreakerInfo:
    """Class representing various information of the quadgrams for a given language"""

    def __init__(self, alphabet=None, nbr_quadgrams=None, most_frequent_quadgram=None, average_fitness=None, max_fitness=None):
        self.alphabet = alphabet
        self.nbr_quadgrams = nbr_quadgrams
        self.most_frequent_quadgram = most_frequent_quadgram
        self.average_fitness = average_fitness
        self.max_fitness = max_fitness

class BreakerResult:
    """Class representing the result for breaking a substitution cipher"""

    def __init__(self, ciphertext=None, plaintext=None, key=None, alphabet=None, fitness=0, nbr_keys=0, nbr_rounds=0, keys_per_second=0, seconds=0):
        self.ciphertext = ciphertext
        self.plaintext = plaintext
        self.key = key
        self.alphabet = alphabet
        self.fitness = fitness
        self.nbr_keys = nbr_keys
        self.nbr_rounds = nbr_rounds
        self.keys_per_second = keys_per_second
        self.seconds = seconds

    def __str__(self):
        return "Key = {}".format(self.key)

class Breaker:
    """Class to represent the breaker implementation based on quadgrams"""

    _DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, quadgram_fh):
        """Init the instance"""
        obj = json.load(quadgram_fh)
        self._alphabet = obj["alphabet"]
        self._alphabet_len = len(self._alphabet)
        self._quadgrams = obj["quadgrams"]
        self.info = BreakerInfo(
            alphabet=obj["alphabet"],
            nbr_quadgrams=obj["nbr_quadgrams"],
            most_frequent_quadgram=obj["most_frequent_quadgram"],
            average_fitness=obj["average_fitness"] / 10,
            max_fitness=obj["max_fitness"] / 10,
        )
        self.key = None

    @staticmethod
    def _text_iterator(txt, alphabet):
        """Implements an iterator for a given text string"""
        trans = {val: key for key, val in enumerate(alphabet.lower())}
        for char in txt.lower():
            val = trans.get(char)
            if val is not None:
                yield val

    def _calc_fitness(self, iterator):
        """Calculate the fitness from the characters provided by the iterator"""
        try:
            # Inicializa el valor del quadgram con los primeros tres caracteres
            quadgram_val = next(iterator)
            quadgram_val = (quadgram_val << 5) + next(iterator)
            quadgram_val = (quadgram_val << 5) + next(iterator)
        except StopIteration:
            raise ValueError("More than three characters from the given alphabet are required")

        fitness = 0
        nbr_quadgrams = 0
        quadgrams = self._quadgrams

        for numerical_char in iterator:
            quadgram_val = ((quadgram_val & 0x7FFF) << 5) + numerical_char
            fitness += quadgrams[quadgram_val]
            nbr_quadgrams += 1

        if nbr_quadgrams == 0:
            raise ValueError("More than three characters from the given alphabet are required")

        return fitness / nbr_quadgrams / 10

    def calc_fitness(self, txt):
        """Method to calculate the fitness for the given text string"""
        return self._calc_fitness(Breaker._text_iterator(txt, self._alphabet))


# --- Example of how to use the Breaker class ---

# Simulating the content of the quadgram file. Replace this with the actual quadgram file.

# Open the quadgram file and create a Breaker instance
# with open("EN.json", "r") as quadgram_fh:
#     breaker = Breaker(quadgram_fh)

# # Example of a plaintext to test
# plaintext = ""

# # Calculate the fitness score for the plaintext
# fitness_score = breaker.calc_fitness(plaintext)
# print(f"Fitness score for the plaintext: {fitness_score}")
