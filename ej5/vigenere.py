import string
from collections import Counter
from itertools import product
from fitness import Breaker  # Importa la clase Breaker del archivo new.py
import time
from concurrent.futures import ThreadPoolExecutor

# Frecuencia de letras en inglés (de mayor a menor frecuencia)
english_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

# Función para dividir el texto en bloques según la longitud de la clave
def divide_text_into_blocks(ciphertext, key_length):
    blocks = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        blocks[i % key_length] += char
    return blocks

# Función para obtener una lista de desplazamientos más probables usando el análisis de frecuencias
def get_key_letter_candidates(block, num_candidates=3):
    block_counter = Counter(block)
    
    # Lista para almacenar las letras clave más probables
    candidates = []
    
    # Ordena las letras más comunes en el bloque
    most_common_letters = block_counter.most_common()
    
    # Siempre selecciona 'E' como la letra más frecuente para eliminar la aleatoriedad
    frequent_letter = 'E'

    # Calcula los desplazamientos probables basados en las letras más comunes en inglés
    for i in range(min(num_candidates, len(most_common_letters))):
        most_common_letter = most_common_letters[i][0]
        # El desplazamiento se calcula con respecto a la letra más frecuente 'E'
        shift = (string.ascii_uppercase.index(most_common_letter) - string.ascii_uppercase.index(frequent_letter)) % 26
        candidates.append(string.ascii_uppercase[shift])
    
    return candidates

# Función para generar todas las combinaciones de claves probables
def generate_probable_keys(blocks, num_candidates=3):
    # Obtener listas de candidatos por cada bloque
    candidate_letters = [get_key_letter_candidates(block, num_candidates) for block in blocks]
    
    # Generar todas las combinaciones posibles de las claves
    probable_keys = [''.join(key) for key in product(*candidate_letters)]
    
    return probable_keys

# Función para descifrar un texto cifrado con Vigenère
def vigenere_decrypt(ciphertext, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    decrypted_text = []
    key_length = len(key)
    key_as_int = [alphabet.index(k) for k in key]
    ciphertext_int = [alphabet.index(c) for c in ciphertext]
    
    for i in range(len(ciphertext_int)):
        # Desencriptamos restando el valor de la clave
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        decrypted_text.append(alphabet[value])
    
    # Devuelve el texto en mayúsculas y sólo con caracteres válidos
    return ''.join(decrypted_text).upper()

# Función para evaluar una clave con el fitness
def evaluate_key(ciphertext, key, breaker):
    decrypted_text = vigenere_decrypt(ciphertext, key)
    
    if len(decrypted_text) < 4:
        return key, -float('inf')  # Si el texto es demasiado corto, no tiene sentido evaluarlo
    
    try:
        fitness_score = breaker.calc_fitness(decrypted_text)
        return key, fitness_score
    except ValueError:
        return key, -float('inf')  # En caso de error, devolver puntaje muy bajo

# Función para evaluar las claves generadas utilizando multithreading
def evaluate_keys(ciphertext, probable_keys, breaker, num_threads=4):
    key_fitness_scores = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(evaluate_key, ciphertext, key, breaker) for key in probable_keys]
        
        for future in futures:
            key, fitness_score = future.result()
            if fitness_score > -float('inf'):
                key_fitness_scores.append((key, fitness_score))
    
    # Ordenar las claves por el puntaje de fitness en orden descendente
    key_fitness_scores.sort(key=lambda x: x[1], reverse=True)
    
    return key_fitness_scores

# Tiempo de inicio
start_time = time.time()

# Texto cifrado
ciphertext = ("KCCPKBGUFDPHQTYAVINRRTMVGRKDNBVFDETDGILTXRGUDDKOTFMBPVGEGLTGCKQRACQCWDNAWCRXIZAKFTLEWRPTYCQKYVXCHKFTPONCQQRHJVAJUWETMCMSPKQDYHJVDAHCTRLSVSKCGCZQQDZXGSFRLSWCWSJTBHAFSIASPRJAHKJRJUMVGKMITZHFPDISPZLVLGWTFPLKKEBDPGCEBSHCTJRWXBAFSPEZQNRWXCVYCGAONWDDKACKAWBBIKFTIOVKCGGHJVLNHIFFSQESVYCLACNVRWBBIREPBBVFEXOSCDYGZWPFDTKFQIYCWHJVLNHIQIBTKHJVNPIST")

# Longitud de clave obtenida (6 en este caso)
key_length = 6

# Dividir el texto en bloques de longitud de clave
blocks = divide_text_into_blocks(ciphertext, key_length)

# Generar todas las claves más probables
probable_keys = generate_probable_keys(blocks, num_candidates=5)
print(f"Total de claves generadas: {len(probable_keys)}")

# Tiempo después de la generación de claves
gen_time = time.time()

# Crear una instancia de Breaker (usando un archivo de quadgramas previamente generado)
with open("EN.json", "r") as quadgram_fh:
    breaker = Breaker(quadgram_fh)

# Evaluar las claves generadas y obtener las 5 mejores basadas en el fitness
key_fitness_scores = evaluate_keys(ciphertext, probable_keys, breaker, num_threads=8)

# Tiempo final después de evaluar las claves
end_time = time.time()

# Mostrar las 5 claves con mejor puntaje de fitness
print("Top 5 claves más probables basadas en el fitness:")
for i, (key, score) in enumerate(key_fitness_scores[:5]):
    print(f"Clave {i+1}: {key} | Fitness: {score}")

# Imprimir los tiempos de ejecución
print(f"Tiempo de generación de claves: {gen_time - start_time:.2f} segundos")
print(f"Tiempo de evaluación de claves: {end_time - gen_time:.2f} segundos")
print(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")
