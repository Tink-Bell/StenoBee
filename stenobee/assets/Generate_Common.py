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
    # Extract words and lowercase them for ranking,
    # removing trailing "'s" from raw text tokens.
    tokens = re.findall(r"\b[A-Za-z]+(?:'\w+)?\b", text)
    processed = []
    for w in tokens:
        lower = w.lower()
        # strip trailing "'s" specifically
        if lower.endswith("'s"):
            lower = lower[:-2]
        processed.append(lower)
    return processed

# --- Encoding utilities ---
letter_order = "XKPMSHLTJQCNRDGFVBZ-OAEI"
vowel_mapping = {
    'W': 'OA', 'U': 'OI', 'Y': 'EI'
}
# The standard uppercase suffix sequence
suffix_sequence = ['JQ', 'XQ', 'QZ', 'KQ', 'QV', 'XJQ', 'JQZ', 'KJQ', 'JQV', 'XJQZ', 'JQVZ', 'XKJQ', 'KJQV']


def replace_characters(word):
    # Word passed in should be uppercase
    return ''.join(vowel_mapping.get(ch, ch) for ch in word)


def combine_suffix(input_string):
    if '/' not in input_string:
        return input_string
    base, suffix = input_string.split('/')
    combined = ''.join(sorted(base + suffix))
    return ''.join(c for c in letter_order if c in combined)

# --- Core encoding function ---

def encode_word(word, encoded_words, encoded_suffix_words):
    orig = word  # preserve original case for mapping
    proc = replace_characters(unidecode(word).upper())
    encoded = []
    vowel_seen = False
    for letter in letter_order:
        if letter == '-' or letter in proc:
            if letter in vowel_mapping:
                if vowel_seen:
                    encoded.append('-')
                vowel_seen = True
            encoded.append(letter)
    enc_str = ''.join(encoded)
    if not vowel_seen:
        enc_str = enc_str.rstrip('-')

    # Assign base or suffix on collision
    if enc_str not in encoded_words:
        encoded_words[enc_str] = orig
        return enc_str, None
    for suffix in suffix_sequence:
        candidate = f"{enc_str}/{suffix}"
        if candidate not in encoded_words and combine_suffix(candidate) not in encoded_suffix_words:
            encoded_words[candidate] = orig
            encoded_suffix_words[combine_suffix(candidate)] = orig
            return enc_str, suffix
    return None, None  # overflow

# --- Main workflow ---

def main():
    parser = argparse.ArgumentParser(
        description='Convert raw text to ranked words and encode into StenoBee JSON, preserving required/extras casing.')
    parser.add_argument('-r', '--raw_input', default='user_raw_common.txt', help='Raw input text file')
    parser.add_argument('-a', '--append_file', default='required_common.txt', help='File with required words (preserve case)')
    parser.add_argument('-e', '--extras_file', default='extras_common.txt', help='File with extra words/phrases (preserve case)')
    parser.add_argument('-o', '--output_json', default='StenoBee-Common.json', help='Output JSON file')
    parser.add_argument('-f', '--overflow_file', default='overflow.txt', help='Overflow output file')
    args = parser.parse_args()

    # Verify input files exist
    for fname in (args.raw_input, args.append_file, args.extras_file):
        if not os.path.isfile(fname):
            print(f"Error: '{fname}' not found.")
            sys.exit(1)

    # Step 1: Filter raw text lines by vowel content
    filtered_lines = []
    with open(args.raw_input, 'r') as f:
        for line in f:
            if any(has_vowels(w) for w in line.strip().split()):
                filtered_lines.append(line)
    raw_text = ''.join(filtered_lines)

    # Step 2: Rank words by frequency (ignoring case for raw text)
    ranked_raw = list(OrderedDict(sorted(Counter(tokenize_text(raw_text)).items(), key=lambda x: -x[1])).keys())

    # Step 3: Load required and extra lists (preserve case)
    def load_list(path):
        with open(path, 'r') as f:
            return [l.strip() for l in f if l.strip()]
    required = load_list(args.append_file)
    extras = load_list(args.extras_file)

    # Step 4: Exclude from raw any words present in required (case-insensitive)
    required_lower = set(w.lower() for w in required)
    ranked = [w for w in ranked_raw if w not in required_lower]

    # Step 5: Exclude from extras any words present in required or raw (case-insensitive)
    raw_lower = set(ranked)
    extras_filtered = [w for w in extras if w.lower() not in required_lower and w.lower() not in raw_lower]

    # Step 6: Combine required -> raw -> extras lists without duplicates
    combined = []
    for w in required + ranked + extras_filtered:
        if w not in combined:
            combined.append(w)

    # Step 7: Encode all words
    encoded_words = OrderedDict()
    encoded_suffix_words = {}
    overflow = []
    suffix_log = []
    for w in combined:
        base_enc, suffix = encode_word(w, encoded_words, encoded_suffix_words)
        if base_enc is None:
            overflow.append(w)
        elif suffix:
            suffix_log.append((base_enc, suffix))

    # Step 8: Generate repeated '/JQ' variants
    for base_enc, suffix in suffix_log:
        idx = suffix_sequence.index(suffix)
        if idx > 0:
            rep = '/'.join(['JQ'] * (idx + 1))
            rep_key = f"{base_enc}/{rep}"
            if rep_key not in encoded_words:
                encoded_words[rep_key] = encoded_words[f"{base_enc}/{suffix}"]

    # Step 9: Write overflow list
    with open(args.overflow_file, 'w') as f:
        for w in overflow:
            f.write(f"{w}\n")

    # Step 10: Output JSON with combined and repeated-JQ entries
    with open(args.output_json, 'w') as f:
        f.write('{' + '\n')
        keys = list(encoded_words.keys())
        for i, key in enumerate(keys):
            val = encoded_words[key]
            f.write(f'"{key}": "{val}"')
            if '/' in key and key.count('/') == 1:
                combined_key = combine_suffix(key)
                f.write(',\n')
                f.write(f'"{combined_key}": "{val}"')
            if i < len(keys) - 1:
                f.write(',\n')
        f.write('\n}')

    print(f"Processing complete. Output saved to {args.output_json}")

if __name__ == '__main__':
    main()

