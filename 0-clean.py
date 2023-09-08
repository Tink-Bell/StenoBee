import argparse

def has_vowels(word):
    vowels = "AEIOUYWaeiouyw"
    return any(char in vowels for char in word)

def filter_vowelless_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            words = line.strip().split()
            filtered_words = [word for word in words if has_vowels(word)]
            if filtered_words:
                outfile.write(" ".join(filtered_words) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Remove lines with vowelless words from a text file.")
    parser.add_argument("input_file", help="Name of the input file")
    parser.add_argument("output_file", help="Name of the output file")

    args = parser.parse_args()

    filter_vowelless_lines(args.input_file, args.output_file)
    print(f"Words without vowels removed. Output saved to '{args.output_file}'")

if __name__ == "__main__":
    main()

