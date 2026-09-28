import sys
import json
import random
import os

def shuffle_dictionary_entry(data):
    if "entries" not in data or not isinstance(data.get("entries"), list):
        print("No valid 'entries' list found in JSON.")
        return data

    question_id_counter = 1

    for entry in data["entries"]:
        if not isinstance(entry, dict):
            continue

        # Shuffle bullet_points within the entry
        if "bullet_points" in entry and isinstance(entry["bullet_points"], list):
            random.shuffle(entry["bullet_points"])

        # Shuffle questions within the entry
        if "questions" in entry and isinstance(entry["questions"], list):
            random.shuffle(entry["questions"])
            for q in entry["questions"]:
                if isinstance(q, dict):
                    q["id"] = str(question_id_counter)
                    question_id_counter += 1

    print("Successfully shuffled bullet_points and questions within each entry.")
    return data

def process_file(file_path):
    print(f"Processing {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict) and data.get("type") == "dictionary_entry":
            data = shuffle_dictionary_entry(data)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {os.path.basename(file_path)}.")
        else:
            print(f"Skipping {os.path.basename(file_path)}: type is not 'dictionary_entry'.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 shuffle_dictionary_entry.py <path_to_json_file_or_directory>")
        sys.exit(1)

    target_path = sys.argv[1]

    if os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in sorted(files):
                if file.endswith(".json"):
                    process_file(os.path.join(root, file))
    elif os.path.isfile(target_path):
        process_file(target_path)
    else:
        print(f"Error: Target path '{target_path}' does not exist.")
        sys.exit(1)

if __name__ == "__main__":
    main()
