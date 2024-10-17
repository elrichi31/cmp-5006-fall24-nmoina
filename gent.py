import re

# Texto encriptado
encrypted_text = """
EMGLOSUDCGDNCUSWYSFHNSFCYKDPUMLWGYICOXYSIPJCK
QPKUGKMGOLICGINCGACKSNISACYKZSCKXECJCKSHYSXCG
OIDPKZCNKSHICGIWYGKKGKGOLDSILKGOIUSIGLEDSPWZU
GFZCCNDGYYSFUSZCNXEOJNCGYEOWEUPXEZGACGNFGLKNS
ACIGOIYCKXCJUCIUZCFZCCNDGYYSFEUEKUZCSOCFZCCNC
IACZEJNCSHFZEJZEGMXCYHCJUMGKUCY
"""

# Frecuencia de letras estimada para inglés (descendente)
english_frequencies = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

# Frecuencias del texto cifrado (descendente basado en el análisis)
cipher_frequencies = 'CGSKYIUNZEOFDLXJPWMHAQ'

# Crear un diccionario para las sustituciones (mapeo inicial basado en frecuencias)
substitution_map = {cipher_frequencies[i]: english_frequencies[i] for i in range(len(cipher_frequencies))}

substitution_map2 = {cipher_frequencies[i]: english_frequencies[i] for i in range(len(cipher_frequencies))}

substitution_map3 = {cipher_frequencies[i]: cipher_frequencies[i] for i in range(len(cipher_frequencies))}

# Función para hacer la sustitución
def substitute(text, mapping):
    # Realizar la sustitución letra por letra
    result = []
    for letter in text:
        if letter in mapping:
            result.append(mapping[letter])  # Reemplazar si está en el diccionario
        else:
            result.append(letter)  # Mantener la letra original (p.ej., saltos de línea)
    return ''.join(result)

# Texto con sustituciones iniciales
decrypted_text = substitute(encrypted_text, substitution_map)

decrypted_text2 = substitute(encrypted_text, substitution_map3)

print("Texto con sustituciones iniciales:")
print(decrypted_text2)

# Mostrar resultado inicial
print("Texto con sustituciones iniciales:")
print(decrypted_text)

# Función para permutar letras manualmente y mostrar el nuevo texto descifrado
def update_substitution(cipher_letter, plain_letter):
    # Actualizar el mapeo de sustituciones
    substitution_map2[cipher_letter] = plain_letter
    # Generar el texto actualizado con las nuevas sustituciones
    updated_text = substitute(encrypted_text, substitution_map2)
    return updated_text

# Aplicar permutaciones manuales
decrypted_text = update_substitution('Z', 'H')
decrypted_text = update_substitution('F', 'W')
decrypted_text = update_substitution('N', 'L')
decrypted_text = update_substitution('G', 'A')
decrypted_text = update_substitution('S', 'N')
decrypted_text = update_substitution('K', 'S')
decrypted_text = update_substitution('L', 'Y')
decrypted_text = update_substitution('U', 'T')
decrypted_text = update_substitution('Y', 'R')
decrypted_text = update_substitution('M', 'M')
decrypted_text = update_substitution('E', 'I')
decrypted_text = update_substitution('J', 'C')
decrypted_text = update_substitution('S', 'O')
decrypted_text = update_substitution('H', 'F')
decrypted_text = update_substitution('X', 'P')
decrypted_text = update_substitution('O', 'V')
#wheel
#always
#love
#master
#perfect
#vehicle



# Aplicar nueva sustitución y mostrar el resultado final
print("\nTexto final con todas las sustituciones aplicadas:")
print(decrypted_text)
