from unidecode import unidecode
import sys
import os

# Define the letter order and vowel mapping
letter_order = "^XKPMSHLTJQCNRDGFVBZ-OAEI"
vowel_mapping = {
'W': 'OA',	'U': 'OI',	'Y': 'EI',
'w': 'OA',	'u': 'OI',	'y': 'EI',
}

# Function to encode a word
def encode_word(word):
    encoded_word = ""
    found_vowel_group = False

    for letter in letter_order:
        if letter == '-' or letter in word:
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

    return encoded_word  # Change this line to return a string instead of a list

def transform_text(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("{\n")

        for line in infile:
            # Remove leading and trailing whitespaces from the line
            line = line.strip()

            # Convert to uppercase
            encoded = unidecode(line.upper().replace(' ', '/^'))

            # if line doesn't have a space, then first letter needs a / to break it off
            if not '/' in encoded:
                encoded = encoded[0] + '/^' + encoded[1:]

            # for letter duplicate reasons, the WUY needs to be handled here
            encoded = encoded.replace('W', '<oa').replace('U', '<oi').replace('Y', '<ei')



            # breakup segments more if duplicate letter found
            encoded_parts = encoded.split('/')
            for i, part in enumerate(encoded_parts):
                # Check for repeated characters within each part
                new_part = ''
                j = 0
                seen_letters = set()  # Keep track of letters seen in the current segment
                while j < len(part):
                    current_letter = part[j]
                    new_part += current_letter
                    if current_letter in seen_letters:
                        if j >= 2 and part[j-2] == "<" and (part[j] == "a" or part[j] == "i"):
                            new_part = new_part[:-2] + '/^' + new_part[-2:] + current_letter
                        else:
                            new_part = new_part + '/^' + current_letter
                        seen_letters.clear()
                    else:
                        seen_letters.add(current_letter)
                    j += 1
                new_part = new_part.replace('<', '')
                encoded_parts[i] = new_part.upper()
            encoded = '/^'.join(encoded_parts)





            # order the letters in each segment by the letter order
            encoded_parts = encoded.split('/')
            for i, part in enumerate(encoded_parts):
                if i > 0:
                    encoded_parts[i] = encode_word("^" + part)
                encoded_parts[i] = encode_word(part)

            # Join the modified parts back together
            encoded = '/'.join(encoded_parts)

            # Write to the output file in the desired format
            outfile.write(f'"{encoded}": "{line}",\n')

        outfile.seek(outfile.tell() - 2, os.SEEK_SET)
        outfile.write("\n}")

if __name__ == "__main__":
    input_filename = "user_list_proper.txt"  # Change this to the actual input file name
    output_filename = "StenoBee-Proper-Nouns.json"  # Change this to the desired output file name

    transform_text(input_filename, output_filename)

