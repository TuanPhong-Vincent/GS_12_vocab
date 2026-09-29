#!/usr/bin/env python3
"""
Compile modular grammar exercise JSON files into a consolidated grammar_raw.json,
or split an existing grammar_raw.json into individual modular exercise files.
"""

import os
import sys
import json
import re
import argparse

EXERCISE_MAP = [
    ("01_mcq.json", "ex1_mcq"),
    ("02_verbform.json", "ex2_verbform"),
    ("03_matching.json", "ex3_matching"),
    ("04_rewrite.json", "ex4_rewrite"),
    ("05_guided_cloze.json", "ex5_guided_cloze"),
    ("06_error_identification.json", "ex6_error_identification"),
    ("07_sentence_combination.json", "ex7_sentence_combination"),
    ("08_sentence_building.json", "ex8_sentence_building"),
]

def count_questions(exercise_data):
    """Accurately counts questions in an exercise object."""
    if "questions" in exercise_data and isinstance(exercise_data["questions"], list):
        return len(exercise_data["questions"])
    if "passages" in exercise_data and isinstance(exercise_data["passages"], list):
        return sum(len(p.get("questions", [])) for p in exercise_data["passages"])
    if "pairs" in exercise_data and isinstance(exercise_data["pairs"], list):
        return len(exercise_data["pairs"])
    return 0

def detect_unit_info(lesson_path):
    """Infers grade and unit number from file path or directory names."""
    unit_num = 1
    grade_str = "GS12"

    unit_match = re.search(r'unit[_-]?(\d+)', lesson_path, re.IGNORECASE)
    if unit_match:
        unit_num = int(unit_match.group(1))

    grade_match = re.search(r'(GS\d{2})', lesson_path, re.IGNORECASE)
    if grade_match:
        grade_str = grade_match.group(1).upper()

    return grade_str, unit_num

def compile_grammar_raw(lesson_folder):
    """Compiles individual 01_*.json files into grammar_raw.json."""
    exercises_dir = os.path.join(lesson_folder, "grammar", "exercises")
    if not os.path.exists(exercises_dir):
        # Fallback to grammar/ or lesson_folder/
        if os.path.exists(os.path.join(lesson_folder, "grammar")):
            exercises_dir = os.path.join(lesson_folder, "grammar")
        else:
            exercises_dir = lesson_folder

    print(f"Scanning for grammar exercises in: {exercises_dir}")
    grade_str, unit_num = detect_unit_info(lesson_folder)

    compiled_exercises = {}
    total_questions = 0
    grammar_topic = "Target Grammar"
    unit_theme = f"Unit {unit_num}"

    # Search for files
    for filename, ex_key in EXERCISE_MAP:
        target_file = None
        # Check in exercises_dir
        candidate = os.path.join(exercises_dir, filename)
        if os.path.exists(candidate):
            target_file = candidate
        else:
            # Check prefix match (e.g. 01_*.json)
            prefix = filename.split("_")[0] + "_"
            for f in os.listdir(exercises_dir):
                if f.startswith(prefix) and f.endswith(".json"):
                    target_file = os.path.join(exercises_dir, f)
                    break

        if target_file and os.path.exists(target_file):
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    ex_data = json.load(f)
                compiled_exercises[ex_key] = ex_data
                q_count = count_questions(ex_data)
                total_questions += q_count
                print(f"  [+] Loaded {os.path.basename(target_file)} -> {ex_key} ({q_count} questions)")

                if "target_grammar" in ex_data:
                    grammar_topic = ex_data["target_grammar"]
            except Exception as e:
                print(f"  [-] Error loading {target_file}: {e}")

    if not compiled_exercises:
        print("Warning: No exercise JSON files were found to compile.")
        return None

    raw_output = {
        "grade": grade_str,
        "unit": unit_num,
        "unit_theme": unit_theme,
        "grammar_topic": grammar_topic,
        "total_exercises": len(compiled_exercises),
        "total_questions": total_questions,
        "exercises": compiled_exercises
    }

    # Save to grammar/grammar_raw.json and lesson_folder/grammar_raw.json
    out_paths = [
        os.path.join(lesson_folder, "grammar", "grammar_raw.json"),
        os.path.join(lesson_folder, "grammar_raw.json")
    ]

    for out_path in out_paths:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(raw_output, f, ensure_ascii=False, indent=2)
        print(f"[OK] Wrote consolidated file ({total_questions} questions) to: {out_path}")

    return raw_output

def split_grammar_raw(raw_path, output_dir):
    """Splits a consolidated grammar_raw.json into individual 01_*.json files."""
    if not os.path.exists(raw_path):
        print(f"Error: File not found: {raw_path}")
        return False

    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    exercises = data.get("exercises", {})
    if not exercises:
        print("No 'exercises' key found in grammar_raw.json")
        return False

    os.makedirs(output_dir, exist_ok=True)

    rev_map = {ex_key: filename for filename, ex_key in EXERCISE_MAP}

    for ex_key, ex_content in exercises.items():
        filename = rev_map.get(ex_key, f"{ex_key}.json")
        target_path = os.path.join(output_dir, filename)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(ex_content, f, ensure_ascii=False, indent=2)
        print(f"  [+] Unpacked {ex_key} -> {target_path}")

    print(f"[OK] Successfully unpacked {len(exercises)} exercises to {output_dir}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Compile or split grammar exercise JSON files.")
    parser.add_argument("path", help="Path to unit folder (for compile) or grammar_raw.json (for split)")
    parser.add_argument("--split", action="store_true", help="Split grammar_raw.json into individual files")
    parser.add_argument("--output-dir", default=None, help="Output directory when splitting")

    args = parser.parse_args()

    if args.split:
        out_dir = args.output_dir or os.path.join(os.path.dirname(os.path.abspath(args.path)), "grammar", "exercises")
        split_grammar_raw(args.path, out_dir)
    else:
        compile_grammar_raw(args.path)

if __name__ == "__main__":
    main()
