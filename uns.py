import re
from collections import Counter

# Ciphertext proporcionado (sin especificar)
ciphertext = '''
BNVSNSIHQCEELSSKKYERIFJKXUMBGYKAMQLJTYAVFBKVTDVBPVVRJYYLAOKYMPQSCGDLFSRLLPROYGESEBUUALRWXMMASAZLGLEDFJBZAVVPXWICGJXASCBYEHOSNMULKCEAHTQOKMFLEBKFXLRRFDTZXCIWBJSICBGAWDVYDHAVFJXZIBKCGJIWEAHTTOEWTUHKRQVVRGZBXYIREMMASCSPBNLHJMBLRFFJELHWEYLWISTFVVYFJCMHYUYRUFSFMGESIGRLWALSWMNUHSIMYYITCCQPZSICEHBCCMZFEGVJYOCDEMMPGHVAAUMELCMOEHVLTIPSUYILVGFLMVWDVYDBTHFRAYISYSGKVSUUHYHGGCKTMBLRX
'''.replace('\n', '')

# Limpiar el texto cifrado
clean_text = re.sub(r'[^A-Z]', '', ciphertext.upper())

# Total number of letters in the ciphertext
total_letters = len(clean_text)

# Calcular la frecuencia de letras individuales
single_freq = Counter(clean_text)
single_freq_percent = {k: (v / total_letters * 100) for k, v in single_freq.items()}

# Mostrar las frecuencias de las letras
print("Frecuencias de letras:\n")
for letter, freq in sorted(single_freq_percent.items(), key=lambda x: x[1], reverse=True):
    print(f"{letter}: {freq:.2f}%")
