import os
import json
import shutil

source_dir = os.path.dirname(__file__)
destination_dir = os.path.join(source_dir, '../../src/maps')

def choose_json_files():
    json_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]
    if not json_files:
        print("No JSON files found in the directory.")
        return []
    print("Available JSON files:")
    for idx, file in enumerate(json_files):
        print(f"{idx + 1}. {file}")
    print(f"{len(json_files) + 1}. Select all")
    choice = input("Choose a number (or multiple numbers separated by commas): ")
    if choice.strip() == str(len(json_files) + 1):
        return json_files
    else:
        try:
            selected_indices = [int(i.strip()) - 1 for i in choice.split(',')]
            return [json_files[i] for i in selected_indices if 0 <= i < len(json_files)]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return []

def validate_json_files(file_list):
    valid_files = []
    for file in file_list:
        file_path = os.path.join(source_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for key, value in data.items():
                pass
            valid_files.append(file)
        except json.JSONDecodeError:
            print(f"Error: {file} contains invalid JSON.")
        except Exception as e:
            print(f"Unexpected error with {file}: {e}")
    return valid_files

def copy_valid_json_files(valid_files):
    os.makedirs(destination_dir, exist_ok=True)
    for file in valid_files:
        src = os.path.join(source_dir, file)
        dst_name = "new_world.json" if file == "world.json" else file
        dst = os.path.join(destination_dir, dst_name)
        shutil.copy2(src, dst)
        print(f"Copied {file} to {destination_dir} as {dst_name}")

def main():
    files_to_check = choose_json_files()
    if files_to_check:
        valid_files = validate_json_files(files_to_check)
        if valid_files:
            copy_valid_json_files(valid_files)
        else:
            print("No valid JSON files to copy.")
    else:
        print("No files selected.")

if __name__ == "__main__":
    main()