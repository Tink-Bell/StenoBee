import sys

# Define the letter order and vowel mapping
letter_order = "KXCFDSHQTPBJNGRLZMV-AEIO"
vowel_mapping = {
    'y': 'AE',
    'u': 'EI',
    'w': 'IO',
}

# Function to replace characters in a word
def replace_characters(word):
    result = ""
    for char in word:
        if char in vowel_mapping:
            result += vowel_mapping[char]
        else:
            result += char
    return result

# Function to encode a word
def encode_word(word, encoded_words):
    word = replace_characters(word)  # Replace characters before encoding
    original_word = word
    encoded_word = ""
    found_vowel_group = False

    for letter in letter_order:
        if letter == '-' or letter.lower() in word.lower():
            if letter in vowel_mapping.keys():
                if found_vowel_group:
                    encoded_word += "-"
                found_vowel_group = True
                encoded_word += letter
            else:
                encoded_word += letter

    # Remove trailing '-' if there are no vowels in the word
    if not found_vowel_group:
        encoded_word = encoded_word.rstrip('-')

    if encoded_word in encoded_words:
        # If the encoded word already exists, generate a unique suffix
        suffix = 'QJ'  # Start with the first suffix
        while f"{encoded_word}/{suffix}" in encoded_words:
            suffix = next_suffix(suffix)
        if suffix == None:
            return None
        else:
            encoded_suffix = f"{encoded_word}/{suffix}"
        
        # Add the new encoded word with the suffix to the dictionary
        encoded_words[encoded_suffix] = original_word

        return [encoded_suffix]

    else:
        encoded_words[encoded_word] = original_word

    return [encoded_word]


# Function to generate the next suffix in the sequence
def next_suffix(suffix):
    if suffix == 'QJ':
        return 'QX'
    elif suffix == 'QX':
        return 'QZ'
    elif suffix == 'QZ':
        return 'QK'
    elif suffix == 'QK':
        return 'VQ'
    elif suffix == 'VQ':
        return 'QF'
    elif suffix == 'QF':
        return 'QH'
    else:
        return None

# Check for command-line arguments
if len(sys.argv) != 3:
    print("Usage: python script_name.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read the list of words from the input file
with open(input_file, 'r') as f:
    words = [line.strip() for line in f]

# Create a dictionary to store the encoded words
encoded_words = {}

# Encode the words and store them in the dictionary
for word in words:
    encoded_versions = encode_word(word, encoded_words)
    if encoded_versions == None:
        continue
    for encoded_word in encoded_versions:
        if encoded_word:
            encoded_words[encoded_word] = word

# Write the encoded words to the output file
with open(output_file, 'w') as f:
    for encoded_word, original_word in sorted(encoded_words.items()):
        if '/' in encoded_word:
            # Write two lines for words with suffixes
            suffix, encoded = encoded_word.split('/')
            combined_suffix = ''.join(sorted(suffix + encoded))
            combined_suffix_ordered = ''.join([c for c in letter_order if c in combined_suffix])
            f.write(f'"{encoded_word}": "{original_word}",\n')
            f.write(f'"{combined_suffix_ordered}": "{original_word}",\n')
        else:
            f.write(f'"{encoded_word}": "{original_word}",\n')

print("Encoding complete. Output saved to", output_file)

