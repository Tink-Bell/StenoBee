import sys
import re
from collections import Counter

# Function to tokenize text into words
def tokenize_text(text):
    # Use regular expression to split text into words based on spaces, periods, !, or ?
    words = re.findall(r"\b(?:[A-Za-z]+(?:'\w+)?)\b", text.lower())
    return words

# Function to count word frequencies and return a ranked list
def rank_words(text):
    # Tokenize the input text
    words = tokenize_text(text)

    # Count the frequency of each word
    word_counts = Counter(words)

    # Sort the words by frequency in descending order
    ranked_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    return ranked_words

# Function to write ranked words to an output file
def write_ranked_words(ranked_words, output_file, include_numbers=True):
    with open(output_file, 'w') as file:
        for word, frequency in ranked_words:
            if include_numbers or not any(char.isdigit() for char in word):
                file.write(f'{word}\n')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python word_frequency_counter.py input_file output_file [include_numbers]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    include_numbers = True
    if len(sys.argv) >= 4 and sys.argv[3].lower() == "false":
        include_numbers = False

    # Read the input text from the input file
    with open(input_file, 'r') as file:
        input_text = file.read()

    # Get the ranked words
    ranked_words = rank_words(input_text)

    # Write ranked words to the output file
    write_ranked_words(ranked_words, output_file, include_numbers)

