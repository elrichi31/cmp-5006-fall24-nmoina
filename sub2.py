import re
from collections import Counter
import random
import json
import math

# Provided ciphertext
ciphertext = '''
EMGLOSUDCGDNCUSWYSFHNSFCYKDPUMLWGYICOXYSIPJCK
QPKUGKMGOLICGINCGACKSNISACYKZSCKXECJCKSHYSXCG
OIDPKZCNKSHICGIWYGKKGKGOLDSILKGOIUSIGLEDSPWZU
GFZCCNDGYYSFUSZCNXEOJNCGYEOWEUPXEZGACGNFGLKNS
ACIGOIYCKXCJUCIUZCFZCCNDGYYSFEUEKUZCSOCFZCCNC
IACZEJNCSHFZEJZEGMXCYHCJUMGKUCY
'''

# Clean the ciphertext: remove non-alphabetic characters and convert to uppercase
clean_text = re.sub(r'[^A-Z]', '', ciphertext.upper())

# Calculate the frequency of individual letters in the ciphertext
single_freq = Counter(clean_text)

# English letter frequency (most to least frequent)
english_freq = list('ETAOINSHRDLCUMWFGYPBVKJXQZ')

# Define the alphabet and create a mapping from letter to index
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter_to_index = {letter: i for i, letter in enumerate(alphabet)}

# Function to create the initial key as a list of 26 letters (a permutation of the alphabet)
def create_initial_key():
    key = [''] * 26
    # Sort the ciphertext letters by frequency
    sorted_cipher_letters = [letter for letter, freq in sorted(single_freq.items(), key=lambda x: x[1], reverse=True)]
    used_plain_letters = set()

    # Map the most frequent letters in the ciphertext to the most frequent English letters
    for i, cipher_letter in enumerate(sorted_cipher_letters):
        cipher_index = letter_to_index[cipher_letter]
        plain_letter = english_freq[i]
        # Assign the letter if it has not been used already
        if plain_letter not in used_plain_letters:
            key[cipher_index] = plain_letter
            used_plain_letters.add(plain_letter)
        else:
            # Assign an unused letter if the plain letter is already used
            for letter in english_freq:
                if letter not in used_plain_letters:
                    key[cipher_index] = letter
                    used_plain_letters.add(letter)
                    break

    # Assign any remaining letters that have not been used yet
    for i in range(26):
        if key[i] == '':
            for letter in english_freq:
                if letter not in used_plain_letters:
                    key[i] = letter
                    used_plain_letters.add(letter)
                    break
            else:
                # Use the remaining letters from the alphabet if english_freq letters are exhausted
                for letter in alphabet:
                    if letter not in used_plain_letters:
                        key[i] = letter
                        used_plain_letters.add(letter)
                        break
    return key

# Function to apply the key to the ciphertext and get the plaintext
def apply_key(ciphertext, key):
    plaintext = ''
    # Replace each letter in the ciphertext with its corresponding letter in the key
    for c in ciphertext:
        index = letter_to_index[c]
        plaintext += key[index]
    return plaintext

# Function to swap two letters in the key
def swap_letters(key, index1, index2):
    # Create a copy of the key and swap the letters at the given indices
    new_key = key.copy()
    new_key[index1], new_key[index2] = new_key[index2], new_key[index1]
    return new_key

# Function to calculate the fitness score using quadgrams
def calc_fitness(txt, quadgrams, alphabet):
    # Create a mapping of each character to a numerical value
    trans = {val: key for key, val in enumerate(alphabet.lower())}
    
    # Iterator to convert text into numerical values
    def text_iterator(txt):
        for char in txt.lower():
            val = trans.get(char)
            if val is not None:
                yield val

    iterator = text_iterator(txt)
    
    # Calculate initial quadgram value using the first three characters
    try:
        quadgram_val = next(iterator)
        quadgram_val = (quadgram_val << 5) + next(iterator)
        quadgram_val = (quadgram_val << 5) + next(iterator)
    except StopIteration:
        raise ValueError("More than three characters from the given alphabet are required")

    fitness = 0
    nbr_quadgrams = 0

    # Compute fitness score using quadgrams
    for numerical_char in iterator:
        quadgram_val = ((quadgram_val & 0x7FFF) << 5) + numerical_char
        # If quadgram exists, add its score; otherwise, penalize
        if quadgram_val < len(quadgrams):
            fitness += quadgrams[quadgram_val]
        else:
            fitness += -10 
        nbr_quadgrams += 1

    if nbr_quadgrams == 0:
        raise ValueError("More than three characters from the given alphabet are required")

    # Normalize the fitness score by the number of quadgrams
    return fitness / nbr_quadgrams / 10

# Function for simulated annealing to optimize the key
def decrypt(ciphertext, initial_key, quadgrams, alphabet, max_iterations=8000, temp=1.0, cooling_rate=0.995, restart_threshold=700):
    current_key = initial_key.copy()
    current_plaintext = apply_key(ciphertext, current_key)
    current_fitness = calc_fitness(current_plaintext, quadgrams, alphabet)
    best_key = current_key.copy()
    best_fitness = current_fitness
    print(f"Initial fitness score: {current_fitness}")

    no_improvement_count = 0

    # Iteratively attempt to improve the key
    for iteration in range(max_iterations):
        temp *= cooling_rate

        # Swap two random positions in the key
        index1, index2 = random.sample(range(26), 2)
        new_key = swap_letters(current_key, index1, index2)
        new_plaintext = apply_key(ciphertext, new_key)
        new_fitness = calc_fitness(new_plaintext, quadgrams, alphabet)

        # Decide whether to accept the new key based on fitness
        if new_fitness > current_fitness:
            accept = True
            no_improvement_count = 0
        else:
            delta = new_fitness - current_fitness
            probability = math.exp(delta / temp)
            accept = random.random() < probability
            no_improvement_count += 1

        # Update the current key if accepted
        if accept:
            current_key = new_key.copy()
            current_fitness = new_fitness

            # Update the best key if the new fitness is better
            if current_fitness > best_fitness:
                best_key = current_key.copy()
                best_fitness = current_fitness
                print(f"Iteration {iteration}: New best fitness score: {best_fitness}")
        
        # Restart with a random key if no improvement after many iterations
        if no_improvement_count >= restart_threshold:
            current_key = list(alphabet)
            random.shuffle(current_key)
            current_plaintext = apply_key(ciphertext, current_key)
            current_fitness = calc_fitness(current_plaintext, quadgrams, alphabet)
            no_improvement_count = 0
            temp = 2.0

    return best_key, best_fitness

# Function to print the comparison of the key with the alphabet
def print_key_comparison(key):
    print("\nAlphabet: ", ' '.join(alphabet))
    print("Key     : ", ' '.join(key))

# Load quadgram data from the JSON file
with open("EN.json", "r") as quadgram_fh:
    quadgram_data = json.load(quadgram_fh)
    alphabet = quadgram_data["alphabet"]
    quadgrams = quadgram_data["quadgrams"]

# Create the initial key based on frequency analysis
initial_key = create_initial_key()

# Apply the initial key to decrypt the ciphertext
initial_plaintext = apply_key(clean_text, initial_key)

# Calculate the fitness score for the initial decryption
initial_fitness = calc_fitness(initial_plaintext, quadgrams, alphabet)

# Display the initial key, decrypted text, and its fitness score
print("\nInitial key based on frequency analysis:")
print_key_comparison(initial_key)
print("\nInitial plaintext:\n", initial_plaintext)
print(f"\nInitial fitness score: {initial_fitness}")

# Optimize the key using simulated annealing
optimized_key, optimized_fitness = decrypt(clean_text, initial_key, quadgrams, alphabet)

# Apply the optimized key to decrypt the ciphertext
optimized_plaintext = apply_key(clean_text, optimized_key)

# Display the optimized plaintext, fitness score, and key comparison
print("\nOptimized plaintext:\n", optimized_plaintext)
print(f"\nOptimized fitness score: {optimized_fitness}")

print_key_comparison(optimized_key)
