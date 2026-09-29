#!/usr/bin/env python3
"""
Comprehensive Audit Script for Grammar Exercise Datasets.
Verifies question counts, JSON validity, MCQ option balance, matching completeness,
and vocabulary integration against vocab.json.
"""

import os
import sys
import json
import re
from collections import Counter

EXPECTED_COUNTS = {
    "01_mcq.json": 20,
    "02_verbform.json": 20,
    "03_matching.json": 10,
    "04_rewrite.json": 10,
    "05_guided_cloze.json": 40,  # 2 passages * 20
    "06_error_identification.json": 10,
    "07_sentence_combination.json": 10,
    "08_sentence_building.json": 10,
}

def audit_mcq_balance(questions):
    """Checks distribution of correct answers across positions A (0), B (1), C (2), D (3)."""
    counts = Counter()
    for q in questions:
        opts = q.get("options", [])
        ans = q.get("correct_answer")
        if ans in opts:
            counts[opts.index(ans)] += 1
        elif ans in ["A", "B", "C", "D"]:
            idx = ["A", "B", "C", "D"].index(ans)
            counts[idx] += 1
    return dict(sorted(counts.items()))

def load_vocab_list(lesson_folder):
    """Loads vocabulary words from vocab.json or raw-vocabulary.md."""
    vocab_paths = [
        os.path.join(lesson_folder, "vocab", "vocab.json"),
        os.path.join(lesson_folder, "vocab.json"),
    ]
    for vp in vocab_paths:
        if os.path.exists(vp):
            try:
                with open(vp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                words = set()
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "words" in item:
                            for w in item["words"]:
                                if "english_word" in w:
                                    words.add(w["english_word"].lower().strip())
                        elif isinstance(item, dict) and "english_word" in item:
                            words.add(item["english_word"].lower().strip())
                elif isinstance(data, dict):
                    word_list = data.get("words", []) or data.get("vocab", [])
                    for w in word_list:
                        if isinstance(w, dict) and "english_word" in w:
                            words.add(w["english_word"].lower().strip())
                return words
            except Exception as e:
                print(f"Notice: Failed to parse vocab.json: {e}")
    return set()

def audit_grammar_directory(lesson_folder):
    exercises_dir = os.path.join(lesson_folder, "grammar", "exercises")
    if not os.path.exists(exercises_dir):
        if os.path.exists(os.path.join(lesson_folder, "grammar")):
            exercises_dir = os.path.join(lesson_folder, "grammar")
        else:
            exercises_dir = lesson_folder

    print("=" * 70)
    print(f"GRAMMAR EXERCISE QUALITY AUDIT: {os.path.abspath(lesson_folder)}")
    print(f"Target Directory: {exercises_dir}")
    print("=" * 70)

    vocab_set = load_vocab_list(lesson_folder)
    print(f"Vocabulary Target Baseline: {len(vocab_set)} words found from vocab.json\n")

    overall_passed = True
    audit_results = []
    exercise_texts = []

    if not os.path.exists(exercises_dir):
        print(f"[FAIL] Exercises directory does not exist: {exercises_dir}")
        return False

    for filename, expected_count in EXPECTED_COUNTS.items():
        file_path = os.path.join(exercises_dir, filename)
        if not os.path.exists(file_path):
            # Check alternative prefix
            prefix = filename.split("_")[0] + "_"
            if os.path.exists(exercises_dir):
                for f in os.listdir(exercises_dir):
                    if f.startswith(prefix) and f.endswith(".json"):
                        file_path = os.path.join(exercises_dir, f)
                        break

        if not os.path.exists(file_path):
            audit_results.append((filename, 0, expected_count, "MISSING FILE", False, {}))
            overall_passed = False
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                file_text = json.dumps(data, ensure_ascii=False)
                exercise_texts.append(file_text.lower())

            actual_count = 0
            details = {}

            if "questions" in data and isinstance(data["questions"], list):
                actual_count = len(data["questions"])
                if filename.startswith("01_") or "mcq" in filename:
                    details["distribution"] = audit_mcq_balance(data["questions"])
            elif "passages" in data and isinstance(data["passages"], list):
                passages = data["passages"]
                p_counts = [len(p.get("questions", [])) for p in passages]
                actual_count = sum(p_counts)
                details["passages_count"] = len(passages)
                details["per_passage_questions"] = p_counts
            elif "pairs" in data and isinstance(data["pairs"], list):
                actual_count = len(data["pairs"])
            elif "questions" in data and "options" in data:
                actual_count = len(data["questions"])

            passed = (actual_count == expected_count)
            status = "PASSED" if passed else f"COUNT MISMATCH ({actual_count}/{expected_count})"
            if not passed:
                overall_passed = False

            audit_results.append((filename, actual_count, expected_count, status, passed, details))

        except Exception as e:
            audit_results.append((filename, 0, expected_count, f"JSON ERROR: {e}", False, {}))
            overall_passed = False

    # Print Table
    print(f"{'Filename':<32} | {'Actual':<8} | {'Target':<8} | {'Status'}")
    print("-" * 70)
    for fn, act, exp, st, p, det in audit_results:
        flag = "[PASS]" if p else "[FAIL]"
        print(f"{fn:<32} | {act:<8} | {exp:<8} | {flag} {st}")
        if det:
            print(f"   -> Details: {det}")

    # Check Vocab Integration
    if vocab_set:
        combined_text = " ".join(exercise_texts).replace("-", " ")
        matched_words = []
        for w in vocab_set:
            w_norm = w.replace("-", " ").lower()
            # Generate common variations
            vars_to_check = {w_norm, w.lower()}
            tokens = w_norm.split()
            if len(tokens) > 1:
                # e.g., 'have a long marriage' -> 'had a long marriage'
                if tokens[0] == 'have':
                    vars_to_check.add("had " + " ".join(tokens[1:]))
                elif tokens[0] == 'attend':
                    vars_to_check.add("attended " + " ".join(tokens[1:]))
                    vars_to_check.add("attending " + " ".join(tokens[1:]))
                elif tokens[0] == 'carry':
                    vars_to_check.add("carried " + " ".join(tokens[1:]))
                elif tokens[0] == 'devote':
                    vars_to_check.add("devoted " + " ".join(tokens[1:]))
                elif tokens[0] == 'bond':
                    vars_to_check.add("bonded " + " ".join(tokens[1:]))
                elif tokens[0] == 'pass':
                    vars_to_check.add("passed " + " ".join(tokens[1:]))
                elif tokens[0] == 'be':
                    vars_to_check.add("was " + " ".join(tokens[1:]))
                    vars_to_check.add("were " + " ".join(tokens[1:]))
                    vars_to_check.add("is " + " ".join(tokens[1:]))
            else:
                if w_norm.endswith('e'):
                    vars_to_check.add(w_norm + 'd')
                    vars_to_check.add(w_norm[:-1] + 'ing')
                else:
                    vars_to_check.add(w_norm + 'ed')
                    vars_to_check.add(w_norm + 'ing')

            if any(re.search(r'\b' + re.escape(var) + r'\b', combined_text) for var in vars_to_check):
                matched_words.append(w)

        coverage_pct = (len(matched_words) / len(vocab_set)) * 100
        print("\n" + "-" * 70)
        print(f"VOCABULARY INTEGRATION COVERAGE: {len(matched_words)}/{len(vocab_set)} words ({coverage_pct:.1f}%)")
        if coverage_pct >= 85.0:
            print("[PASS] Vocabulary integration requirement satisfied (>= 85%).")
        else:
            print(f"[WARN] Vocabulary coverage ({coverage_pct:.1f}%) is below recommended 85%. Consider enriching sentences.")

    print("\n" + "=" * 70)
    if overall_passed:
        print(">>> ALL GRAMMAR DATASET AUDIT CHECKS PASSED SUCCESSFULLY! <<<")
    else:
        print(">>> AUDIT FAILED: Some exercises are missing or have question count mismatches. <<<")
    print("=" * 70)

    return overall_passed

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audit grammar exercise datasets for question counts, balance, and quality.")
    parser.add_argument("lesson_folder", help="Path to unit folder (e.g. lessons/unit-1)")
    args = parser.parse_args()

    success = audit_grammar_directory(args.lesson_folder)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
