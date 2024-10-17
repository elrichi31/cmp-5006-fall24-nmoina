import re
from collections import Counter

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

# Display single-letter frequencies sorted by frequency
print("Single-letter frequencies (percentage):\n")
for letter, freq in sorted(single_freq_percent.items(), key=lambda x: x[1], reverse=True):
    print(f"{letter}: {freq:.2f}%")

# Calculate bigram frequencies
bigrams = [clean_text[i:i+2] for i in range(len(clean_text) - 1)]
bigram_freq = Counter(bigrams)

# Display top 10 most common bigrams
print("\nTop 10 bigrams:\n")
for bigram, count in bigram_freq.most_common(10):
    print(f"{bigram}: {count}")

# Calculate trigram frequencies
trigrams = [clean_text[i:i+3] for i in range(len(clean_text) - 2)]
trigram_freq = Counter(trigrams)

# Display top 10 most common trigrams
print("\nTop 10 trigrams:\n")
for trigram, count in trigram_freq.most_common(10):
    print(f"{trigram}: {count}")
