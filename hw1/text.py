# Define input and output file names
input_file = "20k.txt"   # Replace with your actual file name
output_file = "filtered_words.txt"

# Read and filter words
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for word in infile:
        word = word.strip()  # Remove any extra spaces or newline characters
        if len(word) >= 5:   # Check if word is at least 5 letters long
            outfile.write(word + "\n")  # Write to the output file

print(f"Filtered words saved to {output_file}")