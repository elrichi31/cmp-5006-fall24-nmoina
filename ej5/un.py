from collections import Counter
from itertools import product
import string
import time

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
def evaluate_key(ciphertext, key, quadgrams, alphabet):
    decrypted_text = vigenere_decrypt(ciphertext, key)
    
    if len(decrypted_text) < 4:
        return key, -float('inf')  # Si el texto es demasiado corto, no tiene sentido evaluarlo
    
    try:
        # Llamada a la función calc_fitness proporcionada
        fitness_score = calc_fitness(decrypted_text, quadgrams, alphabet)
        return key, fitness_score
    except ValueError:
        return key, -float('inf')  # En caso de error, devolver puntaje muy bajo

# Evaluar las claves generadas sin concurrencia
def evaluate_keys(ciphertext, probable_keys, quadgrams, alphabet):
    key_fitness_scores = []
    
    # Evaluar cada clave secuencialmente
    for key in probable_keys:
        key, fitness_score = evaluate_key(ciphertext, key, quadgrams, alphabet)
        if fitness_score > -float('inf'):
            key_fitness_scores.append((key, fitness_score))
    
    # Ordenar las claves por el puntaje de fitness en orden descendente
    key_fitness_scores.sort(key=lambda x: x[1], reverse=True)
    
    return key_fitness_scores

# Texto cifrado
ciphertext = ("BNVSNSIHQCEELSSKKYERIFJKXUMBGYKAMQLJTYAVFBKVTDVBPVVRJYYLAOKYMPQSCGDLFSRLLPROYGESEBUUALRWXMMASAZLGLEDFJBZAVVPXWICGJXASCBYEHOSNMULKCEAHTQOKMFLEBKFXLRRFDTZXCIWBJSICBGAWDVYDHAVFJXZIBKCGJIWEAHTTOEWTUHKRQVVRGZBXYIREMMASCSPBNLHJMBLRFFJELHWEYLWISTFVVYFJCMHYUYRUFSFMGESIGRLWALSWMNUHSIMYYITCCQPZSICEHBCCMZFEGVJYOCDEMMPGHVAAUMELCMOEHVLTIPSUYILVGFLMVWDVYDBTHFRAYISYSGKVSUUHYHGGCKTMBLRX")

# Longitud de clave obtenida (6 en este caso)
key_length = 6

# Dividir el texto en bloques de longitud de clave
blocks = divide_text_into_blocks(ciphertext, key_length)

# Generar todas las claves más probables
probable_keys = generate_probable_keys(blocks, num_candidates=5)
print(f"Total de claves generadas: {len(probable_keys)}")

# Asume que 'quadgrams' y 'alphabet' ya están definidos y cargados
quadgrams = ...  # Cargar quadgrams desde un archivo o definirlos
alphabet = string.ascii_uppercase

# Evaluar las claves generadas y obtener las 5 mejores basadas en el fitness
key_fitness_scores = evaluate_keys(ciphertext, probable_keys, quadgrams, alphabet)

# Mostrar las 5 claves con mejor puntaje de fitness
print("Top 5 claves más probables basadas en el fitness:")
for i, (key, score) in enumerate(key_fitness_scores[:5]):
    print(f"Clave {i+1}: {key} | Fitness: {score}")
