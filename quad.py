import json
import string
from collections import Counter
import random

# Función para contar los quadgrams en un corpus de texto
def count_quadgrams(text):
    # Limpiar el texto: quitar caracteres no alfabéticos y convertir a minúsculas
    cleaned_text = ''.join([char for char in text.lower() if char in string.ascii_lowercase])
    quadgram_counts = Counter()

    # Contar los quadgrams
    for i in range(len(cleaned_text) - 3):
        quadgram = cleaned_text[i:i+4]
        quadgram_counts[quadgram] += 1

    return quadgram_counts

# Función para convertir quadgrams a una lista de frecuencias de tamaño 26^4
def quadgrams_to_list(quadgram_counts):
    # Lista de 26^4 (456,976) elementos inicializados en 0
    quadgram_list = [0] * (26 ** 4)
    alphabet = string.ascii_lowercase
    
    # Convertir cada quadgram a su índice correspondiente y asignar la frecuencia
    for quadgram, count in quadgram_counts.items():
        # Calcular el índice para cada quadgram
        index = (
            (ord(quadgram[0]) - ord('a')) * 26**3 +
            (ord(quadgram[1]) - ord('a')) * 26**2 +
            (ord(quadgram[2]) - ord('a')) * 26 +
            (ord(quadgram[3]) - ord('a'))
        )
        quadgram_list[index] = count

    return quadgram_list

# Función para aumentar el tamaño de la lista de quadgrams
def extend_quadgram_list(quadgram_list, target_size=1000000, min_val=0, max_val=2000):
    # Genera valores adicionales para alcanzar el tamaño deseado
    additional_values = [random.randint(min_val, max_val) for _ in range(target_size - len(quadgram_list))]
    # Combina la lista existente con los valores adicionales
    extended_list = quadgram_list + additional_values
    return extended_list

# Cargar un corpus de texto (reemplaza 'corpus.txt' con tu archivo de texto extenso)
with open('corpus.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Contar los quadgrams
quadgram_counts = count_quadgrams(text)

# Convertir a una lista de frecuencias de tamaño 26^4
quadgram_list = quadgrams_to_list(quadgram_counts)

# Extender la lista de quadgrams a aproximadamente 1 millón de elementos
# quadgram_list = extend_quadgram_list(quadgram_list)

# Calcular las estadísticas requeridas
total_quadgrams = sum(quadgram_list)
most_frequent_quadgram = max(quadgram_counts, key=quadgram_counts.get)
max_fitness = max(quadgram_list)
average_fitness = total_quadgrams / len(quadgram_list)

# Crear el diccionario con la estructura especificada
data = {
    "alphabet": "abcdefghijklmnopqrstuvwxyz",
    "nbr_quadgrams": total_quadgrams,
    "most_frequent_quadgram": most_frequent_quadgram,
    "max_fitness": max_fitness,
    "average_fitness": average_fitness,
    "quadgrams": quadgram_list
}

# Convertir a JSON y guardar en un archivo
json_data = json.dumps(data, indent=4)
print(json_data)

# Guardar el JSON en un archivo
with open("large_quadgrams_data.json", "w") as f:
    f.write(json_data)

print("Large quadgrams data saved successfully with approximately 1 million elements.")
