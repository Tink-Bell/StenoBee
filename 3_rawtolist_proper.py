# Function to sort lines by length and remove duplicates
def sort_lines_by_length_and_remove_duplicates(input_file, output_file):
    # Read lines from the input file and remove leading/trailing whitespace
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    # Sort the lines by length and remove duplicates
    sorted_lines = sorted(set(lines), key=len)

    # Write the sorted lines to the output file
    with open(output_file, 'w') as file:
        file.write('\n'.join(sorted_lines))

# Input and output file paths
input_file = 'raw_proper.txt'
output_file = 'list_proper.txt'

# Call the function to sort lines by length and remove duplicates
sort_lines_by_length_and_remove_duplicates(input_file, output_file)

print(f"Lines in '{input_file}' have been sorted by length and duplicates have been removed. Result saved in '{output_file}'.")

