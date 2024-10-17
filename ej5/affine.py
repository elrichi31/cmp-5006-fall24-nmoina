import re
import random
import json
from math import gcd
from fitness import Breaker  # Asegúrate de tener la clase Breaker en fitness.py

# Constantes para el alfabeto inglés
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
M = len(ALPHABET)  # m = 26 para el alfabeto inglés

# Función para calcular el inverso multiplicativo modular
def mod_inverse(a, m):
    """Devuelve el inverso multiplicativo de 'a' módulo 'm' si existe."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Función para descifrar usando Affine Cipher
def affine_decrypt(ciphertext, a, b):
    """Descifra un texto cifrado usando el Affine Cipher con la clave (a, b)."""
    a_inv = mod_inverse(a, M)  # Inverso multiplicativo de a
    if a_inv is None:
        return None  # Si no hay inverso, la clave no es válida

    plaintext = ''
    for char in ciphertext:
        if char in ALPHABET:
            y = ALPHABET.index(char)
            x = (a_inv * (y - b)) % M
            plaintext += ALPHABET[x]
        else:
            plaintext += char  # Dejar cualquier símbolo no alfabético sin cambio
    return plaintext

# Función para probar todas las combinaciones de (a, b)
def break_affine_cipher_iteratively(ciphertext, breaker, max_iterations=10, restart_threshold=100):
    """Prueba todas las combinaciones de a y b iterativamente para romper el Affine Cipher."""
    best_fitness = float('-inf')
    best_plaintext = None
    best_a, best_b = None, None
    improvement_threshold = 0.01  # Cambios mínimos en fitness para detener la iteración
    no_improvement_count = 0

    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        for a in range(1, M):
            if gcd(a, M) != 1:
                continue  # a y m deben ser coprimos
            for b in range(M):
                plaintext = affine_decrypt(ciphertext, a, b)
                if plaintext:
                    fitness = breaker.calc_fitness(plaintext)
                    if fitness > best_fitness + improvement_threshold:
                        best_fitness = fitness
                        best_plaintext = plaintext
                        best_a, best_b = a, b
                        no_improvement_count = 0
                        print(f"New best fitness {fitness} with a={a}, b={b}")
                    else:
                        no_improvement_count += 1

        # Reiniciar si no hay mejora después de restart_threshold intentos
        if no_improvement_count > restart_threshold:
            print(f"Restarting search after {no_improvement_count} combinations with no improvement.")
            no_improvement_count = 0  # Reset counter

        # Si la mejora es muy pequeña o se alcanzó el límite de iteraciones sin mejora, detener
        if no_improvement_count > max_iterations * M:
            print(f"No significant improvement detected, stopping search.")
            break

    return best_plaintext, best_a, best_b, best_fitness

# Ciphertext proporcionado (Affine Cipher)
ciphertext = '''
KQEREJEBCPPCJCRKIEACUZBKRVPKRBCIBQCARBJCVFCUPKRIOFKPACUZQEPBKRXPEIIEABDKPBCPFCDCCAFIEABDKPBCPFEQPKAZBKRHAIBKAPCCIBURCCDKDCCJCIDFUIXPAFFERBICZDFKABICBBENEFCUPJCVKABPCYDCCDPKBCOCPERKIVKSCPICBRKIJPKABI
'''.replace('\n', '')

# Limpiar el texto cifrado
clean_text = re.sub(r'[^A-Z]', '', ciphertext.upper())

# Abrir el archivo de quadgrams y crear una instancia del Breaker
with open("EN.json", "r") as quadgram_fh:
    breaker = Breaker(quadgram_fh)

# Romper el Affine Cipher iterativamente
best_plaintext, best_a, best_b, best_fitness = break_affine_cipher_iteratively(clean_text, breaker)

# Mostrar los resultados finales
print(f"\nBest plaintext: {best_plaintext}")
print(f"Best a: {best_a}, Best b: {best_b}")
print(f"Best fitness score: {best_fitness}")
