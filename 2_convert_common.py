import sys
import os

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
        if suffix is None:
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
        return 'XQ'
    elif suffix == 'XQ':
        return 'QZ'
    elif suffix == 'QZ':
        return 'KQ'
    elif suffix == 'KQ':
        return 'QV'
    elif suffix == 'QV':
        return 'FQ'
    elif suffix == 'FQ':
        return 'HQ'
    else:
        return None

# Check for command-line arguments
if len(sys.argv) != 1:
    print("Usage: python script_name.py")
    sys.exit(1)

input_file_append = "required_common.txt"
input_file_list = "user_list_common.txt"
input_file_phrases = "extras_common.txt"
output_file = "StenoBee-Common.json"

# Check if the input files exist
if not os.path.isfile(input_file_append):
    print(f"Error: The input file '{input_file_append}' does not exist.")
    sys.exit(1)
if not os.path.isfile(input_file_list):
    print(f"Error: The input file '{input_file_list}' does not exist.")
    sys.exit(1)
if not os.path.isfile(input_file_phrases):
    print(f"Error: The input file '{input_file_phrases}' does not exist.")
    sys.exit(1)

# Read the list of words from the input files
with open(input_file_append, 'r') as f:
    append_words = [line.strip() for line in f]

with open(input_file_list, 'r') as f:
    list_words = [line.strip() for line in f]

with open(input_file_phrases, 'r') as f:
    phrases_words = [line.strip() for line in f]

# Combine the words from keeping the original order and removing duplicates
combined_words = []

# Function to add words to the combined list while removing duplicates
def add_word(word):
    if word not in combined_words:
        combined_words.append(word)

for word in append_words:
    add_word(word)

for word in list_words:
    add_word(word)

for word in phrases_words:
    add_word(word)

# Create a dictionary to store the encoded words
encoded_words = {}

# Encode the words and store them in the dictionary
for word in combined_words:
    encoded_versions = encode_word(word, encoded_words)
    if encoded_versions is None:
        continue
    for encoded_word in encoded_versions:
        if encoded_word:
            encoded_words[encoded_word] = word

# Write the encoded words to the output file
with open(output_file, 'w') as f:
    f.write("{\n")  # Add the opening curly brace
    for i, (encoded_word, original_word) in enumerate(sorted(encoded_words.items())):
        if '/' in encoded_word:
            # Write two lines for words with suffixes
            suffix, encoded = encoded_word.split('/')
            combined_suffix = ''.join(sorted(suffix + encoded))
            combined_suffix_ordered = ''.join([c for c in letter_order if c in combined_suffix])
            f.write(f'"{encoded_word}": "{original_word}",\n')
            f.write(f'"{combined_suffix_ordered}": "{original_word}",\n')
        else:
            f.write(f'"{encoded_word}": "{original_word}"')
            if i < len(encoded_words) - 1:
                f.write(",\n")
    f.write("\n}")  # Add the closing curly brace

print("Converting complete. Output saved to", output_file)

