import argparse
import re
import os
import sys
from collections import Counter, OrderedDict
from unidecode import unidecode

# --- Vowel filtering utilities ---
VOWELS = "AEIOUYWaeiouyw"

def has_vowels(word):
    # Return True if word has at least one vowel but is not all vowels
    return any(c in VOWELS for c in word) and not all(c in VOWELS for c in word)

# --- Text processing utilities ---

def tokenize_text(text):
    # Match words including apostrophes (e.g., don't)
    return re.findall(r"\b(?:[A-Za-z]+(?:'\w+)?)\b", text)

# --- Encoding utilities ---
letter_order = "XKPMSHLTJQCNRDGFVBZ-OAEI"
vowel_mapping = {
    'W': 'OA', 'U': 'OI', 'Y': 'EI',
    'w': 'OA', 'u': 'OI', 'y': 'EI',
}

suffix_sequence = ['JQ', 'XQ', 'QZ', 'KQ', 'QV', 'XJQ', 'JQZ', 'KJQ', 'JQV', 'XJQZ', 'JQVZ', 'XKJQ', 'KJQV']


def replace_characters(word):
    result = []
    for ch in word:
        result.append(vowel_mapping.get(ch, ch))
    return ''.join(result)


def combine_suffix(input_string):
    if '/' not in input_string:
        return input_string
    base, suffix = input_string.split('/')
    combined = ''.join(sorted(base + suffix))
    return ''.join([c for c in letter_order if c in combined])


def next_suffix(current):
    try:
        idx = suffix_sequence.index(current)
        return suffix_sequence[idx + 1]
    except (ValueError, IndexError):
        return None

# --- Core functions ---

def rank_words(text):
    words = tokenize_text(text)
    counts = Counter(words)
    return OrderedDict(sorted(counts.items(), key=lambda x: -x[1]))


def encode_word(word, encoded_words, encoded_suffix_words):
    orig = word
    word = replace_characters(unidecode(word))
    encoded = []
    found_vowel_group = False

    # Build encoding per letter_order
    for letter in letter_order:
        if letter == '-' or letter.lower() in word.lower():
            if letter in vowel_mapping:
                if found_vowel_group:
                    encoded.append('-')
                found_vowel_group = True
            encoded.append(letter)

    enc_str = ''.join(encoded)
    if not found_vowel_group:
        enc_str = enc_str.rstrip('-')

    # Handle duplicates with suffix
    if enc_str in encoded_words:
        suffix = suffix_sequence[0]
        while suffix is not None:
            candidate = f"{enc_str}/{suffix}"
            if candidate not in encoded_words and combine_suffix(candidate) not in encoded_suffix_words:
                enc_str = candidate
                break
            suffix = next_suffix(suffix)
        else:
            return None  # Overflow
        encoded_words[enc_str] = orig
        return [enc_str]
    else:
        encoded_words[enc_str] = orig
        return [enc_str]

# --- Main workflow ---

def main():
    parser = argparse.ArgumentParser(
        description='Process raw text into ranked list and encode into StenoBee JSON.'
    )
    parser.add_argument('-r', '--raw_input', default='user_raw_common.txt',
                        help='Raw input text file')
    parser.add_argument('-a', '--append_file', default='required_common.txt',
                        help='File with required/common words to prepend')
    parser.add_argument('-e', '--extras_file', default='extras_common.txt',
                        help='File with extra phrases/words to append')
    parser.add_argument('-o', '--output_json', default='StenoBee-Common.json',
                        help='Output JSON file')
    parser.add_argument('-f', '--overflow_file', default='overflow.txt',
                        help='Overflow output file')
    args = parser.parse_args()

    # Verify files exist
    for fname in (args.raw_input, args.append_file, args.extras_file):
        if not os.path.isfile(fname):
            print(f"Error: '{fname}' does not exist.")
            sys.exit(1)

    # Read and filter raw text lines
    filtered_lines = []
    with open(args.raw_input, 'r') as f:
        for line in f:
            words = line.strip().split()
            if any(has_vowels(w) for w in words):
                filtered_lines.append(line)

    raw_text = ''.join(filtered_lines)

    # Rank words
    ranked = rank_words(raw_text)
    ranked_list = list(ranked.keys())

    # Read append and extras
    with open(args.append_file, 'r') as f:
        append_words = [l.strip() for l in f if l.strip()]
    with open(args.extras_file, 'r') as f:
        extras_words = [l.strip() for l in f if l.strip()]

    # Combine words without duplicates, preserving order
    combined = []
    def add_word(w):
        if w not in combined:
            combined.append(w)
    for w in append_words + ranked_list + extras_words:
        add_word(w)

    # Encode
    encoded_words = {}
    encoded_suffix_words = {}
    overflow = []
    for w in combined:
        result = encode_word(w, encoded_words, encoded_suffix_words)
        if result is None:
            overflow.append(w)
        else:
            for enc in result:
                if '/' in enc:
                    encoded_suffix_words[combine_suffix(enc)] = w

    # Write overflow
    with open(args.overflow_file, 'w') as f:
        for w in overflow:
            f.write(f"{w}\n")

    # Write JSON
    with open(args.output_json, 'w') as f:
        f.write('{' + '\n')
        items = sorted(encoded_words.items())
        for i, (enc, orig) in enumerate(items):
            line = f'"{enc}": "{orig}"'
            f.write(line)
            if i < len(items) - 1:
                f.write(',\n')
        f.write('\n}')

    print(f"Processing complete. Output saved to {args.output_json}")

if __name__ == '__main__':
    main()

