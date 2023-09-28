# Define the input and output file names
input_file = "user_raw_proper.txt"
output_file = "user_list_proper.txt"

# Function to remove duplicate lines from a list and sort lines with the same length alphabetically
def process_lines(line_list):
    unique_lines = {}
    for line in line_list:
        line_length = len(line.strip())
        if line_length not in unique_lines:
            unique_lines[line_length] = [line]
        else:
            unique_lines[line_length].append(line)

    processed_lines = []
    for length in sorted(unique_lines.keys()):
        lines = unique_lines[length]
        lines.sort()
        processed_lines.extend(lines)

    return processed_lines

# Read the content of the input file and split it into lines
with open(input_file, "r") as file:
    lines = file.readlines()

# Process lines (remove duplicates and sort by length)
processed_lines = process_lines(lines)

# Write the processed lines to the output file
with open(output_file, "w") as file:
    for line in processed_lines:
        file.write(line)

print(f"Cleaned file saved as {output_file}")

