import sys
import json
import random
import math
from collections import Counter

def is_balanced(counts, total_questions):
    """
    Check if the distribution of correct answer indices is balanced.
    For N questions and 4 options:
    The ideal count is N / 4.
    The allowed counts are math.floor(N / 4) and math.ceil(N / 4).
    """
    min_allowed = math.floor(total_questions / 4)
    max_allowed = math.ceil(total_questions / 4)
    
    for i in range(4):
        if counts.get(i, 0) < min_allowed or counts.get(i, 0) > max_allowed:
            return False
    return True

def balance_options(data):
    if "questions" not in data:
        return data
        
    questions = data["questions"]
    
    # Filter only questions with exactly 4 options
    mcq_questions = [q for q in questions if "options" in q and len(q["options"]) == 4 and "correct_answer" in q]
    
    if not mcq_questions:
        print("No valid multiple choice questions (with 4 options) found.")
        return data
        
    total = len(mcq_questions)
    
    attempts = 0
    max_attempts = 10000
    
    while attempts < max_attempts:
        attempts += 1
        
        # Shuffle options for each question
        for q in mcq_questions:
            random.shuffle(q["options"])
            
        # Count indices of correct answers
        counts = Counter()
        for q in mcq_questions:
            try:
                idx = q["options"].index(q["correct_answer"])
                counts[idx] += 1
            except ValueError:
                print(f"Error: correct_answer '{q['correct_answer']}' not found in options {q['options']}")
                return data
                
        if is_balanced(counts, total):
            print(f"Successfully balanced options after {attempts} attempts.")
            print(f"Distribution of correct answer positions (0-3): {dict(counts)}")
            break
    else:
        print(f"Warning: Could not achieve perfect balance after {max_attempts} attempts. Keeping the last shuffle.")
    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 balance_mcq_options.py <path_to_json_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Processing {file_path}...")
        data = balance_options(data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("File successfully updated.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
