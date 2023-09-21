import argparse
import re
from collections import Counter, OrderedDict
import os

def has_vowels(word):
    vowels = "AEIOUYWaeiouyw"
    return any(char in vowels for char in word) and not all(char in vowels for char in word)

def filter_vowelless_lines(input_file):
    cleaned_words = {}
    with open(input_file, 'r') as infile:
        line_count = 0
        for line in infile:
            line_count += 1
            words = line.strip().split()
            filtered_words = [word for word in words if has_vowels(word)]
            if filtered_words:
                cleaned_words[line_count] = filtered_words
    return cleaned_words

def tokenize_text(text):
    words = re.findall(r"\b(?:[A-Za-z]+(?:'\w+)?)\b", text)
    return words

def rank_words(text, cleaned_words):
    words = tokenize_text(text)
    word_counts = Counter(words)
    
    def custom_sort_key(word):
        frequency = -word_counts[word]
        alphabetical_order = word
        return (frequency, alphabetical_order)
    
    ranked_words = OrderedDict(sorted(word_counts.items(), key=lambda x: custom_sort_key(x[0])))
    return ranked_words

def main():
    default_input_file = "user_raw_common.txt"
    default_output_file = "user_list_common.txt"

    parser = argparse.ArgumentParser(description="Remove lines with vowelless or vowel-only words from a text file and rank words by frequency.")
    parser.add_argument("-i", "--input_file", default=default_input_file, help=f"Name of the input file (default: {default_input_file})")
    parser.add_argument("-o", "--output_file", default=default_output_file, help=f"Name of the output file (default: {default_output_file})")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: The input file '{args.input_file}' does not exist.")
        return

    cleaned_words = filter_vowelless_lines(args.input_file)

    with open(args.input_file, 'r') as raw_file:
        raw_text = raw_file.read()

    ranked_words = rank_words(raw_text, cleaned_words)

    with open(args.output_file, 'w') as ranked_file:
        for word in ranked_words:
            ranked_file.write(f'{word}\n')

    print(f"Words Cleaned and Ranked. Output saved to '{args.output_file}'")

if __name__ == "__main__":
    main()

