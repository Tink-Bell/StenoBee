import inflect

LONGEST_KEY = 1  # Replace with the actual value

# Placeholder lookup function
def lookup(stn):
    # This is a placeholder lookup function
    return []

def pluralize_word(word):
    if word.endswith('fe'):
        # wolf -> wolves
        return word[:-2] + 'ves'
    elif word.endswith('f'):
        # knife -> knives
        return word[:-1] + 'ves'
    elif word.endswith('o'):
        # potato -> potatoes
        return word + 'es'
    elif word.endswith('us'):
        # cactus -> cacti
        return word[:-2] + 'i'
    elif word.endswith('on'):
        # criterion -> criteria
        return word[:-2] + 'a'
    elif word.endswith('y'):
        # community -> communities
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word + 's'

def pluralize_keys(keys):
    # Function to pluralize a word based on "S$" keys
    def pluralize_word(word):
        if word == ";FSG$":
            # Replace "S$" with the plural form of the previous word
            if pluralized_words:
                return pluralize_word(pluralized_words[-1])
            else:
                # If no previous word, return as is
                return word
        else:
            return word

    lines = keys.splitlines()  # Split keys into lines
    pluralized_lines = []

    for line in lines:
        words = line.split()  # Split each line into words
        pluralized_words = [pluralize_word(word) for word in words]

        # Join the pluralized words back into a line
        pluralized_line = ' '.join(pluralized_words)
        pluralized_lines.append(pluralized_line)

    # Join the lines back with line breaks
    output_text = '\n'.join(pluralized_lines)
    return output_text

