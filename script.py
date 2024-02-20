import json
import os

def process_localization_files(input_folder, output_jsonl):
    # Use the directory of the script as the base path
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Adjust input_folder and output_jsonl to use the base path
    input_folder_path = os.path.join(base_path, input_folder)
    output_jsonl_path = os.path.join(base_path, output_jsonl)

    # Check if the input folder exists
    if not os.path.exists(input_folder_path):
        print(f"Error: The input folder '{input_folder_path}' does not exist.")
        return

    # Initialize a list to store dictionaries representing jsonl entries
    jsonl_entries = []

    # Language code to human-readable name mapping
    language_mapping = {
        'en': 'English',
        'ru': 'Russian',
        'ja': 'Japanese',
        'pt_BR': 'Brazilian Portuguese',
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish',
        'it': 'Italian',
        'tr': 'Turkish',
        'zh_Hant': 'Traditional Chinese',
        'zh_Hans': 'Simplified Chinese',
        'ko': 'Korean',
        'el': 'Greek',
        'fa': 'Persian'
    }

    # Process each en.json file in the input folder and its subfolders
    for root, _, files in os.walk(input_folder_path):
        for file in files:
            if file == 'en.json':
                source_file_path = os.path.join(root, file)

                # Load the source localization file (en.json)
                with open(source_file_path, 'r', encoding='utf-8') as source_file:
                    try:
                        source_data = json.load(source_file)
                    except json.JSONDecodeError:
                        print(f"Error: Unable to parse JSON file '{source_file_path}'. Skipping.")
                        continue

                    # Process each localization file
                    for target_file in files:
                        if target_file.endswith('.json') and target_file != 'en.json':
                            target_language = os.path.splitext(target_file)[0]  # Extract language from the file name
                            target_file_path = os.path.join(root, target_file)

                            # Open and read the target JSON file
                            with open(target_file_path, 'r', encoding='utf-8') as target_file:
                                try:
                                    target_data = json.load(target_file)
                                except json.JSONDecodeError:
                                    print(f"Error: Unable to parse JSON file '{target_file_path}'. Skipping.")
                                    continue

                                # Create a chat conversation entry for each key-value pair
                                for key, source_text in source_data.items():
                                    user_message = {"role": "user", "content": f"Translate the following phrase to {language_mapping.get(target_language, target_language)}: {source_text}"}
                                    assistant_message = {"role": "assistant", "content": f"Translation: {target_data.get(key, 'N/A')} (Target Language: {language_mapping.get(target_language, target_language)})"}

                                    jsonl_entry = {"messages": [{"role": "system", "content": "You are a multi-language localizer and translator."}, user_message, assistant_message]}
                                    jsonl_entries.append(jsonl_entry)

    # Write the jsonl entries to a JSON Lines file
    with open(output_jsonl_path, 'w', encoding='utf-8') as jsonl_file:
        for entry in jsonl_entries:
            jsonl_file.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"JSON Lines file '{output_jsonl_path}' created successfully!")

# Example usage:
input_folder_name = 'input'
output_jsonl_name = 'output.jsonl'
process_localization_files(input_folder_name, output_jsonl_name)
