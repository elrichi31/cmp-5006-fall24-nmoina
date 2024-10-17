import re
from collections import Counter
import random
import json
import math
# Función simplificada de calc_fitness
def calc_fitness(txt, quadgrams, alphabet):
    """Calculate the fitness for the given text string using quadgrams"""
    # Crear un diccionario para mapear cada letra a un valor numérico
    trans = {val: key for key, val in enumerate(alphabet.lower())}
    
    # Iterador de texto convertido a valores numéricos según el alfabeto
    def text_iterator(txt, alphabet):
        for char in txt.lower():
            val = trans.get(char)
            if val is not None:
                yield val

    # Iterador del texto dado
    iterator = text_iterator(txt, alphabet)
    
    try:
        # Inicializa el valor del quadgram con los primeros tres caracteres
        quadgram_val = next(iterator)
        quadgram_val = (quadgram_val << 5) + next(iterator)
        quadgram_val = (quadgram_val << 5) + next(iterator)
    except StopIteration:
        raise ValueError("More than three characters from the given alphabet are required")

    fitness = 0
    nbr_quadgrams = 0

    # Calcular el puntaje de fitness usando los quadgrams
    for numerical_char in iterator:
        quadgram_val = ((quadgram_val & 0x7FFF) << 5) + numerical_char
        fitness += quadgrams[quadgram_val]
        nbr_quadgrams += 1

    if nbr_quadgrams == 0:
        raise ValueError("More than three characters from the given alphabet are required")

    # Normalizar el fitness por el número de quadgrams y escalarlo
    return fitness / nbr_quadgrams / 10

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

def hill_climbing_optimize_key(ciphertext, initial_key, quadgrams, alphabet, max_iterations=30000, tolerance=0.99, stagnation_limit=50):
    current_key = initial_key
    current_plaintext = apply_key(ciphertext, current_key)
    current_fitness = calc_fitness(current_plaintext, quadgrams, alphabet)
    best_key = current_key
    best_fitness = current_fitness
    max_score = current_fitness  # Variable para mantener el máximo valor de fitness
    print(f"Initial fitness score: {current_fitness}")

    no_improvement_count = 0  # Contador de iteraciones sin mejora
    stagnation_max_scores = []  # Lista para almacenar los máximos tras cada estancamiento

    for iteration in range(1, max_iterations + 1):
        # Swap two random letters in the key
        letter1, letter2 = random.sample(alphabet.upper(), 2)
        new_key = swap_letters(current_key, letter1, letter2)
        new_plaintext = apply_key(ciphertext, new_key)
        new_fitness = calc_fitness(new_plaintext, quadgrams, alphabet)

        # Actualizar el máximo si el nuevo fitness es mejor
        if new_fitness > max_score:
            max_score = new_fitness

        # Decision making based on fitness comparison
        if new_fitness > best_fitness:
            best_key = new_key
            best_fitness = new_fitness
            no_improvement_count = 0  # Resetear el contador de estancamiento
            print(f"Iteration {iteration}: Improved fitness to {best_fitness}")
        
        elif new_fitness == best_fitness:
            # Accept the change with a small probability if the fitness is equal
            if random.random() < tolerance:
                current_key = new_key
                no_improvement_count = 0  # Resetear el contador ya que aceptamos un cambio
                print(f"Iteration {iteration}: Accepted equal fitness {new_fitness} with probability {tolerance}")
            else:
                no_improvement_count += 1
        
        else:
            # Si el nuevo fitness es menor, incrementamos el contador de estancamiento
            no_improvement_count += 1

        # Si hemos alcanzado el límite de estancamiento, realizar una permutación agresiva
        if no_improvement_count >= stagnation_limit:
            print(f"Iteration {iteration}: Stagnation detected. Performing aggressive permutation.")
            stagnation_max_scores.append(max_score)  # Guardar el máximo antes de la permutación

            # Realizar varias permutaciones al azar para intentar salir del estancamiento
            for _ in range(5):  # Realiza 5 permutaciones aleatorias
                letter1, letter2 = random.sample(alphabet.upper(), 2)
                best_key = swap_letters(best_key, letter1, letter2)
            current_plaintext = apply_key(ciphertext, best_key)
            best_fitness = calc_fitness(current_plaintext, quadgrams, alphabet)
            no_improvement_count = 0  # Reiniciar el contador después de la permutación agresiva
            print(f"After permutation, new fitness: {best_fitness}")

            # Actualizar el máximo después de la permutación
            if best_fitness > max_score:
                max_score = best_fitness

    # Almacenar el último máximo después de la última iteración
    stagnation_max_scores.append(max_score)

    # Mostrar los máximos encontrados durante la optimización
    print("\nMax scores reached after each stagnation phase:")
    for idx, score in enumerate(stagnation_max_scores, 1):
        print(f"Stagnation phase {idx}: Fitness score {score}")

    # Mostrar el valor máximo global alcanzado
    overall_max_score = max(stagnation_max_scores)
    print(f"\nOverall max fitness score during optimization: {overall_max_score}")

    # Devolver la mejor clave y su puntaje
    return best_key, best_fitness




# Simulated annealing optimization function with improved restart strategy
def simulated_annealing_optimize_key(ciphertext, initial_key, quadgrams, alphabet, max_iterations=100000, temp=2.0, cooling_rate=0.995, restart_threshold=1000):
    current_key = initial_key
    current_plaintext = apply_key(clean_text, current_key)
    current_fitness = calc_fitness(current_plaintext, quadgrams, alphabet)
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
        new_fitness = calc_fitness(new_plaintext, quadgrams, alphabet)

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
            current_fitness = calc_fitness(current_plaintext, quadgrams, alphabet)
            no_improvement_count = 0
            temp = 2.0  # Reset the temperature for a fresh restart
            print(f"Restarted with new fitness score: {current_fitness}")

    return best_key, best_fitness

# Simulate loading of the quadgram data from a JSON file
with open("EN.json", "r") as quadgram_fh:
    quadgram_data = json.load(quadgram_fh)
    alphabet = quadgram_data["alphabet"]
    quadgrams = quadgram_data["quadgrams"]

# Apply the initial key to the ciphertext
initial_plaintext = apply_key(clean_text, initial_key)

# Calculate the initial fitness score
initial_fitness = calc_fitness(initial_plaintext, quadgrams, alphabet)

# Output the initial key, plaintext, and fitness score
print("\nInitial key based on frequency analysis:\n", initial_key)
print("\nInitial plaintext:\n", initial_plaintext)
print(f"\nInitial fitness score: {initial_fitness}")

# Optimize the key using simulated annealing with the improved strategy
optimized_key, optimized_fitness = hill_climbing_optimize_key(clean_text, initial_key, quadgrams, alphabet)

# Apply the optimized key to the ciphertext
optimized_plaintext = apply_key(clean_text, optimized_key)

# Output the optimized key, plaintext, and fitness score
print("Optimized plaintext:\n", optimized_plaintext)
print(f"\nOptimized fitness score: {optimized_fitness}")

# Print the optimized key compared to the alphabet
def print_key_comparison(key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key_mapping = ''.join(key.get(c, c) for c in alphabet)
    print("\nAlphabet : ", alphabet)
    print("Key      : ", key_mapping)

print_key_comparison(optimized_key)
