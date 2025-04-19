import argparse
import re
import os
import sys
from collections import Counter, OrderedDict
from unidecode import unidecode

# --- Vowel filtering utilities ---
VOWELS = "AEIOUYWaeiouyw"

def has_vowels(word):
    return any(c in VOWELS for c in word) and not all(c in VOWELS for c in word)

# --- Text processing utilities ---

def tokenize_text(text):
    return re.findall(r"\b(?:[A-Za-z]+(?:'\w+)?)\b", text)

# --- Encoding utilities ---
letter_order = "XKPMSHLTJQCNRDGFVBZ-OAEI"
vowel_mapping = {
    'W': 'OA', 'U': 'OI', 'Y': 'EI',
    'w': 'OA', 'u': 'OI', 'y': 'EI',
}
# The standard disambiguation suffix sequence
suffix_sequence = ['JQ', 'XQ', 'QZ', 'KQ', 'QV', 'XJQ', 'JQZ', 'KJQ', 'JQV', 'XJQZ', 'JQVZ', 'XKJQ', 'KJQV']

def replace_characters(word):
    return ''.join(vowel_mapping.get(ch, ch) for ch in word)


def combine_suffix(input_string):
    if '/' not in input_string:
        return input_string
    base, suffix = input_string.split('/')
    combined = ''.join(sorted(base + suffix))
    return ''.join(c for c in letter_order if c in combined)


def next_suffix(current):
    try:
        idx = suffix_sequence.index(current)
        return suffix_sequence[idx + 1]
    except (ValueError, IndexError):
        return None

# --- Core functions ---

def rank_words(text):
    counts = Counter(tokenize_text(text))
    return OrderedDict(sorted(counts.items(), key=lambda x: -x[1]))


def encode_word(word, encoded_words, encoded_suffix_words):
    orig = word
    processed = replace_characters(unidecode(word))
    encoded = []
    found_vowel = False

    for letter in letter_order:
        if letter == '-' or letter.lower() in processed.lower():
            if letter in vowel_mapping:
                if found_vowel:
                    encoded.append('-')
                found_vowel = True
            encoded.append(letter)

    enc_str = ''.join(encoded)
    if not found_vowel:
        enc_str = enc_str.rstrip('-')

    # No collision -> base encoding
    if enc_str not in encoded_words:
        encoded_words[enc_str] = orig
        return enc_str, None

    # Collision: find a suffix from the sequence
    for suffix in suffix_sequence:
        candidate = f"{enc_str}/{suffix}"
        if candidate not in encoded_words and combine_suffix(candidate) not in encoded_suffix_words:
            encoded_words[candidate] = orig
            encoded_suffix_words[combine_suffix(candidate)] = orig
            return enc_str, suffix

    # Overflow
    return None, None

# --- Main workflow ---

def main():
    parser = argparse.ArgumentParser(
        description='Process raw text into ranked list and encode into StenoBee JSON with repeat-JQ disambiguation.')
    parser.add_argument('-r', '--raw_input', default='user_raw_common.txt', help='Raw input text file')
    parser.add_argument('-a', '--append_file', default='required_common.txt', help='File with required words')
    parser.add_argument('-e', '--extras_file', default='extras_common.txt', help='File with extra words/phrases')
    parser.add_argument('-o', '--output_json', default='StenoBee-Common.json', help='Output JSON file')
    parser.add_argument('-f', '--overflow_file', default='overflow.txt', help='Overflow output file')
    args = parser.parse_args()

    # Verify input files exist
    for fname in (args.raw_input, args.append_file, args.extras_file):
        if not os.path.isfile(fname):
            print(f"Error: '{fname}' not found.")
            sys.exit(1)

    # Step 1: Filter raw text lines for vowelless removal
    filtered_lines = []
    with open(args.raw_input, 'r') as f:
        for line in f:
            if any(has_vowels(w) for w in line.strip().split()):
                filtered_lines.append(line)
    raw_text = ''.join(filtered_lines)

    # Step 2: Rank words by frequency
    ranked = list(rank_words(raw_text).keys())

    # Step 3: Load additional lists
    def load_list(path):
        with open(path, 'r') as f:
            return [l.strip() for l in f if l.strip()]
    append_words = load_list(args.append_file)
    extras_words = load_list(args.extras_file)

    # Step 4: Combine lists in order without duplicates
    combined = []
    for w in append_words + ranked + extras_words:
        if w not in combined:
            combined.append(w)

    # Step 5: Encode all words
    encoded_words = OrderedDict()
    encoded_suffix_words = {}
    overflow = []
    # Track base->suffix assignments for repeated JQ
    repeat_info = []  # list of (base_enc, suffix)

    for w in combined:
        base_enc, suffix = encode_word(w, encoded_words, encoded_suffix_words)
        if base_enc is None:
            overflow.append(w)
        elif suffix:
            repeat_info.append((base_enc, suffix))

    # Step 6: Generate repeated '/JQ' variants for non-JQ suffixes
    for base_enc, suffix in repeat_info:
        idx = suffix_sequence.index(suffix)
        if idx > 0:
            # number of repeats = index + 1
            rep = '/'.join(['JQ'] * (idx + 1))
            rep_key = f"{base_enc}/{rep}"
            if rep_key not in encoded_words:
                encoded_words[rep_key] = encoded_words[f"{base_enc}/{suffix}"]

    # Step 7: Write overflow list
    with open(args.overflow_file, 'w') as f:
        for w in overflow:
            f.write(f"{w}\n")

    # Step 8: Write JSON output with combined forms and repeat-JQ lines
    with open(args.output_json, 'w') as f:
        f.write('{' + '\n')
        keys = list(encoded_words.keys())
        for i, key in enumerate(keys):
            val = encoded_words[key]
            # Print raw or repeated suffix entry
            f.write(f'"{key}": "{val}"')
            # If single-suffix (including JQ) -> print combined form
            if '/' in key and key.count('/') == 1:
                combined_key = combine_suffix(key)
                f.write(',\n')
                f.write(f'"{combined_key}": "{val}"')
            # If single-suffix and not repeated, add comma if not last
            if i < len(keys) - 1:
                f.write(',\n')
        f.write('\n}')

    print(f"Processing complete. Output saved to {args.output_json}")

if __name__ == '__main__':
    main()

