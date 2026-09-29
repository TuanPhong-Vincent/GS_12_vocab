#!/usr/bin/env python3
"""
Balance MCQ Option Positions for Grammar Exercises.
Spreads correct answers evenly across positions A (0), B (1), C (2), and D (3).
Supports:
- 01_mcq.json (20 questions -> 5 of each position)
- 05_guided_cloze.json (20 questions per passage -> 5 of each position)
- 06_error_identification.json (10 questions -> ~2-3 of each position)
"""

import os
import sys
import json
import random
import math
from collections import Counter

def is_balanced(counts, total_questions, num_options=4):
    min_allowed = math.floor(total_questions / num_options)
    max_allowed = math.ceil(total_questions / num_options)
    for i in range(num_options):
        if counts.get(i, 0) < min_allowed or counts.get(i, 0) > max_allowed:
            return False
    return True

def balance_question_list(questions, num_options=4, max_attempts=15000):
    mcq_questions = [q for q in questions if "options" in q and len(q["options"]) == num_options and "correct_answer" in q]
    if not mcq_questions:
        return questions

    total = len(mcq_questions)
    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        for q in mcq_questions:
            random.shuffle(q["options"])

        counts = Counter()
        valid = True
        for q in mcq_questions:
            try:
                idx = q["options"].index(q["correct_answer"])
                counts[idx] += 1
            except ValueError:
                valid = False
                break

        if not valid:
            break

        if is_balanced(counts, total, num_options):
            print(f"  [OK] Balanced {total} questions after {attempts} attempts. Distribution: {dict(sorted(counts.items()))}")
            return questions

    print(f"  [WARN] Reached max attempts ({max_attempts}). Current distribution: {dict(sorted(counts.items()))}")
    return questions

def balance_grammar_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    modified = False

    # Standard MCQ structure (e.g. 01_mcq.json)
    if "questions" in data and isinstance(data["questions"], list):
        print(f"Balancing MCQ questions in {os.path.basename(file_path)}...")
        data["questions"] = balance_question_list(data["questions"])
        modified = True

    # Guided Cloze structure (05_guided_cloze.json)
    elif "passages" in data and isinstance(data["passages"], list):
        print(f"Balancing Guided Cloze passages in {os.path.basename(file_path)}...")
        for i, passage in enumerate(data["passages"]):
            if "questions" in passage and isinstance(passage["questions"], list):
                print(f" Passage {i+1} ({passage.get('title', 'Untitled')}):")
                passage["questions"] = balance_question_list(passage["questions"])
                modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved balanced options to {file_path}")
        return True
    else:
        print(f"No balanceable MCQ structures found in {file_path}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Balance Multiple Choice option positions (A, B, C, D) for grammar exercises.")
    parser.add_argument("target", help="Path to JSON file or directory containing grammar exercise JSON files")
    args = parser.parse_args()

    target_path = args.target
    if os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(".json") and any(term in file for term in ["mcq", "cloze", "01_", "05_"]):
                    balance_grammar_file(os.path.join(root, file))
    else:
        balance_grammar_file(target_path)

if __name__ == "__main__":
    main()
