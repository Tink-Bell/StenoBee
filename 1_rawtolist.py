import argparse
import re
from collections import Counter
import os

def has_vowels(word):
    vowels = "AEIOUYWaeiouyw"
    return any(char in vowels for char in word) and not all(char in vowels for char in word)

def filter_vowelless_lines(input_file, cleaned_output_file):
    with open(input_file, 'r') as infile, open(cleaned_output_file, 'w') as outfile:
        for line in infile:
            words = line.strip().split()
            filtered_words = [word for word in words if has_vowels(word)]
            if filtered_words:
                outfile.write(" ".join(filtered_words) + '\n')

def tokenize_text(text):
    words = re.findall(r"\b(?:[A-Za-z]+(?:'\w+)?)\b", text.lower())
    return words

def rank_words(text):
    words = tokenize_text(text)
    word_counts = Counter(words)
    ranked_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return ranked_words

def main():
    default_input_file = "raw.txt"
    default_output_file = "list.txt"

    parser = argparse.ArgumentParser(description="Remove lines with vowelless or vowel-only words from a text file and rank words by frequency.")
    parser.add_argument("-i", "--input_file", default=default_input_file, help=f"Name of the input file (default: {default_input_file})")
    parser.add_argument("-o", "--output_file", default=default_output_file, help=f"Name of the output file (default: {default_output_file})")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: The input file '{args.input_file}' does not exist.")
        return

    cleaned_output_file = "cleaned_" + args.input_file
    filter_vowelless_lines(args.input_file, cleaned_output_file)

    with open(cleaned_output_file, 'r') as cleaned_file:
        cleaned_text = cleaned_file.read()
    
    ranked_words = rank_words(cleaned_text)

    with open(args.output_file, 'w') as ranked_file:
        for word, frequency in ranked_words:
            ranked_file.write(f'{word}\n')

    print(f"Words Cleaned and Ranked . Output saved to '{args.output_file}'")

if __name__ == "__main__":
    main()

