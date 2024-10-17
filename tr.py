import json
import math

def calc_fitness(text, quadgrams):
    fitness = 0.0
    text = text.upper()  # Convert text to uppercase to match quadgrams format
    
    # Iterate through each quadgram in the text
    for i in range(len(text) - 3):
        quadgram = text[i:i+4]  # Get the current sequence of 4 letters
        if quadgram in quadgrams:
            fitness += quadgrams[quadgram]
        else:
            # If the quadgram is not found, add a small penalty for rare or unseen quadgrams
            fitness += math.log10(0.01)  # Penalize for quadgrams that are not common
    
    return fitness

# Cargar el diccionario de quadgrams transformado
with open("new.json", "r") as f:
    quadgrams_dict = json.load(f)

# Ejemplo de texto para evaluar
text = "IMAYNOTHEAHRETOYLOSFROSELRHOTMYYALDENNLODOCERYORTARMANYDEADREATERORDOTELRTOERNIECEROFLONEANDHORTERROFDEADYLARRARANYHODYRANDTODAYIHOOYTTASTEERHALLOSTOTERNINCREALINYITONITATEARSAYRROTEDANDLERNECTEDTTESTEERHALLOSITIRTTEONESTEEREDTETICREOFSTICTIAMNELFECTMARTEL"

# Calcular el puntaje de fitness del texto usando el diccionario transformado
fitness_score = calc_fitness(text, quadgrams_dict)
print(f"Fitness score for the text: {fitness_score}")
