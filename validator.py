import json
import os
import random

def create_validation_file(input_jsonl, output_jsonl):
    # Use the directory of the script as the base path
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Adjust input_jsonl and output_jsonl to use the base path
    input_jsonl_path = os.path.join(base_path, input_jsonl)
    output_jsonl_path = os.path.join(base_path, output_jsonl)

    # Read the input JSON Lines file
    with open(input_jsonl_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # Calculate the number of lines to select (5% of total)
    num_lines_to_select = int(len(lines) * 0.05)

    # Randomly select 5% of the lines
    selected_lines = random.sample(lines, num_lines_to_select)

    # Write the selected lines to the output JSON Lines file
    with open(output_jsonl_path, 'w', encoding='utf-8') as output_file:
        for line in selected_lines:
            output_file.write(line)

    print(f"Validation JSON Lines file '{output_jsonl_path}' created successfully!")

# Example usage:
input_jsonl_name = 'output.jsonl'
output_validation_jsonl_name = 'validation.jsonl'
create_validation_file(input_jsonl_name, output_validation_jsonl_name)
