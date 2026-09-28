import sys
import json
import random

def shuffle_word_box(data):
    if "word_box" in data and isinstance(data["word_box"], list):
        random.shuffle(data["word_box"])
        print("Shuffled word_box.")
    else:
        print("No word_box found in JSON file.")
    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 shuffle_word_box.py <path_to_json_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Processing {file_path}...")
        data = shuffle_word_box(data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("File successfully updated.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
