# Function to sort lines by length and remove duplicates
def sort_lines_by_length_and_remove_duplicates(input_file, output_file):
    # Read lines from the input file and remove leading/trailing whitespace
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    # Sort the lines by length and, in case of equal lengths, alphabetically
    sorted_lines = sorted(lines, key=lambda x: (len(x), x))

    # Remove duplicates
    unique_sorted_lines = []
    seen = set()
    for line in sorted_lines:
        if line not in seen:
            unique_sorted_lines.append(line)
            seen.add(line)

    # Write the sorted lines to the output file
    with open(output_file, 'w') as file:
        file.write('\n'.join(unique_sorted_lines))

# Input and output file paths
input_file = 'user_raw_proper.txt'
output_file = 'user_list_proper.txt'

# Call the function to sort lines by length and remove duplicates
sort_lines_by_length_and_remove_duplicates(input_file, output_file)

print(f"Lines in '{input_file}' have been sorted by length and alphabetically when lengths are equal. Duplicates have been removed. Result saved in '{output_file}'.")

