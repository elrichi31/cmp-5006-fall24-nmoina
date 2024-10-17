import re
from collections import Counter
from itertools import permutations
import random
import json
from fitness import Breaker  # Asegúrate de tener la clase Breaker en fitness.py
import math

# Ciphertext provided
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

# Total number of letters in the ciphertext
total_letters = len(clean_text)

# Calculate single-letter frequency
single_freq = Counter(clean_text)
single_freq_percent = {k: (v / total_letters * 100) for k, v in single_freq.items()}

# English letter frequency (from most frequent to least frequent)
english_freq = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

# Sort cipher letters by frequency
sorted_cipher_letters = [letter for letter, freq in sorted(single_freq.items(), key=lambda x: x[1], reverse=True)]

# Create initial key based on frequency analysis
initial_key = {sorted_cipher_letters[i]: english_freq[i] for i in range(len(sorted_cipher_letters))}

# Function to apply key to ciphertext
def apply_key(ciphertext, key):
    return ''.join([key.get(char, char) for char in ciphertext])

# Function to swap two letters in a key
def swap_letters(key, letter1, letter2):
    new_key = key.copy()
    # Swap the two letters
    for k, v in key.items():
        if v == letter1:
            new_key[k] = letter2
        elif v == letter2:
            new_key[k] = letter1
    return new_key

# Simulated annealing optimization function with improved restart strategy
def simulated_annealing_optimize_key(ciphertext, initial_key, breaker, max_iterations=50000, temp=1.0, cooling_rate=0.995, restart_threshold=700):
    current_key = initial_key
    current_plaintext = apply_key(clean_text, current_key)
    current_fitness = breaker.calc_fitness(current_plaintext)
    best_key = current_key
    best_fitness = current_fitness
    print(f"Initial fitness score: {current_fitness}")

    no_improvement_count = 0

    for iteration in range(max_iterations):
        # Reduce the temperature
        temp *= cooling_rate

        # Swap two random letters in the key
        letter1, letter2 = random.sample(english_freq, 2)
        new_key = swap_letters(current_key, letter1, letter2)
        new_plaintext = apply_key(clean_text, new_key)
        new_fitness = breaker.calc_fitness(new_plaintext)

        # Calculate acceptance probability
        if new_fitness > current_fitness:
            accept = True
            no_improvement_count = 0
        else:
            accept = random.random() < math.exp((new_fitness - current_fitness) / temp)
            no_improvement_count += 1

        if accept:
            current_key = new_key
            current_fitness = new_fitness

            if current_fitness > best_fitness:
                best_key = current_key
                best_fitness = current_fitness
                print(f"New best fitness score: {best_fitness}")
        
        # Random restarts if no improvement after a certain number of iterations
        if no_improvement_count >= restart_threshold:
            print(f"Restarting at iteration {iteration} after no improvement.")
            current_key = {sorted_cipher_letters[i]: random.choice(english_freq) for i in range(len(sorted_cipher_letters))}
            current_plaintext = apply_key(clean_text, current_key)
            current_fitness = breaker.calc_fitness(current_plaintext)
            no_improvement_count = 0
            temp = 2.0  # Reset the temperature for a fresh restart
            print(f"Restarted with new fitness score: {current_fitness}")

    return best_key, best_fitness

# Function to print the key compared to the alphabet
def print_key_comparison(key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key_mapping = ''.join(key.get(c, c) for c in alphabet)
    print("\nAlphabet : ", alphabet)
    print("Key      : ", key_mapping)

# Open the quadgram file and create a Breaker instance
with open("EN.json", "r") as quadgram_fh:
    breaker = Breaker(quadgram_fh)

# Apply the initial key to the ciphertext
initial_plaintext = apply_key(clean_text, initial_key)

# Call the Breaker to evaluate the plaintext fitness
initial_fitness = breaker.calc_fitness(initial_plaintext)

# Output the initial key, plaintext and fitness score
print("\nInitial key based on frequency analysis:\n", initial_key)
print("\nInitial plaintext:\n", initial_plaintext)
print(f"\nInitial fitness score: {initial_fitness}")

# Optimize the key using simulated annealing with improved strategy
optimized_key, optimized_fitness = simulated_annealing_optimize_key(clean_text, initial_key, breaker)

# Apply the optimized key to the ciphertext
optimized_plaintext = apply_key(clean_text, optimized_key)

# Output the optimized key, plaintext and fitness score
print("Optimized plaintext:\n", optimized_plaintext)
print(f"\nOptimized fitness score: {optimized_fitness}")

# Print the optimized key compared to the alphabet
print_key_comparison(optimized_key)
