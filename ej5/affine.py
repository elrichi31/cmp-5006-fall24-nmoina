import re
import random
import json
from math import gcd
from fitness import Breaker  # Ensure that you have the Breaker class in fitness.py

# Constants for the English alphabet
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
M = len(ALPHABET)  # m = 26 for the English alphabet

# Function to calculate the modular multiplicative inverse
def mod_inverse(a, m):
    """Returns the modular multiplicative inverse of 'a' modulo 'm' if it exists."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Function to decrypt using the Affine Cipher
def affine_decrypt(ciphertext, a, b):
    """Decrypts a ciphertext using the Affine Cipher with the key (a, b)."""
    a_inv = mod_inverse(a, M)  # Multiplicative inverse of a
    if a_inv is None:
        return None  # If there is no inverse, the key is invalid

    plaintext = ''
    for char in ciphertext:
        if char in ALPHABET:
            y = ALPHABET.index(char)
            x = (a_inv * (y - b)) % M
            plaintext += ALPHABET[x]
        else:
            plaintext += char  # Keep any non-alphabetic symbols unchanged
    return plaintext

# Function to try all combinations of (a, b)
def break_affine_cipher_iteratively(ciphertext, quadgrams, alphabet, max_iterations=10, restart_threshold=100):
    """Tests all combinations of a and b iteratively to break the Affine Cipher."""
    top_results = []  # Store top five results as tuples (fitness, plaintext, a, b)
    no_improvement_count = 0

    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        for a in range(1, M):
            if gcd(a, M) != 1:
                continue  # a and m must be coprime
            for b in range(M):
                plaintext = affine_decrypt(ciphertext, a, b)
                if plaintext:
                    fitness = calc_fitness(plaintext, quadgrams, alphabet)  # Use the provided calc_fitness function
                    # Store results in a list and keep it sorted to have the top five
                    # Ensure we only add it if it's not a duplicate plaintext in the top results
                    if len(top_results) < 5 or fitness > top_results[-1][0]:
                        if not any(p == plaintext for _, p, _, _ in top_results):
                            # Add the new result and sort the list by fitness (descending)
                            top_results.append((fitness, plaintext, a, b))
                            top_results.sort(reverse=True, key=lambda x: x[0])
                            # Keep only the top five results
                            top_results = top_results[:5]
                            no_improvement_count = 0
                            print(f"New entry in top results: fitness {fitness} with a={a}, b={b}")
                    else:
                        no_improvement_count += 1

        # Restart if no improvement after restart_threshold attempts
        if no_improvement_count > restart_threshold:
            print(f"Restarting search after {no_improvement_count} combinations with no improvement.")
            no_improvement_count = 0  # Reset counter

            # Randomize the starting point for `a` and `b` to diversify the search space
            random.shuffle(top_results)  # Change order to explore different possibilities next

        # If the improvement is minimal or the iteration limit is reached, stop
        if no_improvement_count > max_iterations * M:
            print(f"No significant improvement detected, stopping search.")
            break

    return top_results

# Ciphertext provided (Affine Cipher)
ciphertext = '''
KQEREJEBCPPCJCRKIEACUZBKRVPKRBCIBQCARBJCVFCUPKRIOFKPACUZQEPBKRXPEIIEABDKPBCPFCDCCAFIEABDKPBCPFEQPKAZBKRHAIBKAPCCIBURCCDKDCCJCIDFUIXPAFFERBICZDFKABICBBENEFCUPJCVKABPCYDCCDPKBCOCPERKIVKSCPICBRKIJPKABI
'''.replace('\n', '')

# Clean the ciphertext
clean_text = re.sub(r'[^A-Z]', '', ciphertext.upper())

# Open the quadgram file and create a Breaker instance
with open("./EN.json", "r") as quadgram_fh:
    quadgram_data = json.load(quadgram_fh)
    alphabet = quadgram_data["alphabet"]
    quadgrams = quadgram_data["quadgrams"]

# Break the Affine Cipher iteratively using the provided calc_fitness function
top_results = break_affine_cipher_iteratively(clean_text, quadgrams, alphabet)

# Display the top five results, sorted from highest to lowest fitness
top_results.sort(reverse=True, key=lambda x: x[0])  # Sort by fitness in descending order

print("\nTop 5 Decryption Results:")
for i, (fitness, plaintext, a, b) in enumerate(top_results, 1):
    print(f"\nResult {i}:")
    print(f"Plaintext: {plaintext}")
    print(f"a: {a}, b: {b}")
    print(f"Fitness Score: {fitness}")
