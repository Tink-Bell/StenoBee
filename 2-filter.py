import sys

def contains_required_and_optional_letters(word, required_letters, optional_letters):
    required_found = all(letter in word for letter in required_letters)
    forbidden_found = any(letter not in required_letters + optional_letters for letter in word)
    return required_found and not forbidden_found

def remove_duplicates(words):
    unique_words = []
    seen_words = set()
    for word in words:
        lowercase_word = word.lower()
        if lowercase_word not in seen_words:
            seen_words.add(lowercase_word)
            unique_words.append(word)
    return unique_words

def vowel_breakdown(word):
    vowels = "aeioyuw"
    groups = ["aeio", "yuw"]
    breakdown = []
    for vowel in vowels:
        found_in_group = False
        for group in groups:
            if vowel in group and vowel in word:
                breakdown.append(vowel)
                found_in_group = True
                break
        if not found_in_group:
            breakdown.append("")
    if "y" in breakdown[4] or "u" in breakdown[4] or "w" in breakdown[4]:
        breakdown.insert(4, "\t")
    return "".join(breakdown[:4]) + "\t" + "".join(breakdown[4:])

def main():
    if len(sys.argv) != 5:
        print("Usage: python filter_words.py <input_filename> <output_filename> <required_letters> <optional_letters>")
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    required_letters = sys.argv[3].lower()
    optional_letters = sys.argv[4].lower()

    with open(input_filename, 'r') as file:
        words = file.read().splitlines()

    filtered_words = [word for word in words if contains_required_and_optional_letters(word.lower(), required_letters, optional_letters)]
    unique_words = remove_duplicates(filtered_words)
    
    max_word_length = len(max(unique_words, key=len))

    with open(output_filename, 'w') as file:
        for word in unique_words:
            lowercase_word = word.lower()
            indentation = " " * (max_word_length - len(word))
            vowel_break = vowel_breakdown(lowercase_word)
            file.write(f"{lowercase_word}\n")

    print("Filtering and duplicate removal complete. Filtered words and vowel breakdown saved to", output_filename)

if __name__ == "__main__":
    main()

