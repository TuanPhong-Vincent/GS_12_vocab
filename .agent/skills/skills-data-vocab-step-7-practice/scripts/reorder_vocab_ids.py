import json
import os
import sys

def get_vocab_id(ex_type, title):
    title = title.lower() if title else ""
    if ex_type == "multiple_choice":
        if "direct" in title: return "1"
        if "sentence completion" in title: return "2"
        if "conversation" in title: return "3"
        if "closest" in title: return "9"
        if "opposite" in title: return "10"
        return "1" # fallback
    elif ex_type == "pic_to_word": return "4"
    elif ex_type == "write_english_words": return "5"
    elif ex_type == "fill_in_blanks": return "6"
    elif ex_type == "paragraph_fill": return "7"
    elif ex_type == "sentence_ordering_multiple_choice": return "8"
    elif ex_type == "dictionary_entry": return "11"
    elif ex_type == "signs_and_notices": return "12"
    elif ex_type == "word_families_table": return "13"
    elif ex_type == "word_families_mcq": return "14"
    elif ex_type == "word_formation": return "15"
    elif ex_type == "translate_sentences": return "16"
    return None

def process_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)
        
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, dict) and "type" in data:
                    ex_type = data["type"]
                    title = data.get("title", "")
                    
                    new_id = get_vocab_id(ex_type, title)
                    if new_id:
                        if str(data.get("id")) != new_id:
                            data["id"] = new_id
                            with open(filepath, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            print(f"Updated {filename}: set id to {new_id}")
                        
                        import re
                        base_name = re.sub(r'^\d+_', '', filename)
                        new_filename = f"{int(new_id):02d}_{base_name}"
                        if new_filename != filename:
                            new_filepath = os.path.join(directory, new_filename)
                            os.rename(filepath, new_filepath)
                            print(f"Renamed {filename} to {new_filename}")

            except Exception as e:
                print(f"Failed to process {filename}: {e}")
                
    print("Vocab ID reordering complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 reorder_vocab_ids.py <path_to_vocab_exercises_directory>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    process_directory(target_dir)
