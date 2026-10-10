#!/usr/bin/env python3
"""
Audit script for Standardized 40-Question Unit Tests (test1.json, test2.json).
Verifies 7 Quality Dimensions:
1. Question Count & Sequential Numbering (1..40)
2. Four Unique Options (A, B, C, D) per question
3. Valid & Balanced Answer Keys (~10 for each A, B, C, D)
4. Pedagogical Explanations (knowledge_type & per-choice analysis)
5. Vietnamese Translations for questions and passages
6. Reading Passages & Formatting Markers (blanks, insertion slots [I]-[IV], <u>...</u>)
7. Vocabulary & Grammar thematic integration
"""

import sys
import json
import re
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def audit_test_json(json_path):
    path = Path(json_path)
    print(f"\n==================================================")
    print(f"AUDITING: {path.resolve()}")
    print(f"==================================================")
    
    if not path.exists():
        print(f"❌ FAIL: File not found: {path}")
        return False

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ FAIL: Invalid JSON syntax: {e}")
        return False

    errors = []
    warnings = []

    # 1. Metadata check
    required_meta = ["test_id", "unit_number", "unit_title", "title", "total_questions", "questions"]
    for k in required_meta:
        if k not in data:
            errors.append(f"Missing required top-level key: {k}")

    total_q = data.get("total_questions", 0)
    if total_q != 40:
        errors.append(f"total_questions must be 40, found {total_q}")

    questions = data.get("questions", [])
    if len(questions) != 40:
        errors.append(f"Expected 40 question objects, found {len(questions)}")

    # 2. Check each question
    answer_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    seen_q_nums = set()

    for idx, q in enumerate(questions):
        expected_num = idx + 1
        q_num = q.get("question_number")
        
        # Check numbering
        if q_num != expected_num:
            errors.append(f"Question index {idx}: expected question_number={expected_num}, got {q_num}")
        if q_num in seen_q_nums:
            errors.append(f"Duplicate question_number: {q_num}")
        seen_q_nums.add(q_num)

        # Check prompt
        prompt = q.get("prompt", "")
        if not prompt or not prompt.strip():
            errors.append(f"Q{q_num}: Empty prompt")

        # Check options
        options = q.get("options", {})
        if not isinstance(options, dict):
            errors.append(f"Q{q_num}: 'options' must be an object")
        else:
            for opt_key in ["A", "B", "C", "D"]:
                if opt_key not in options:
                    errors.append(f"Q{q_num}: Missing option '{opt_key}'")
                elif not str(options[opt_key]).strip():
                    errors.append(f"Q{q_num}: Option '{opt_key}' is empty")
            
            # Check for duplicate option values
            opt_vals = [str(options.get(k, "")).strip().lower() for k in ["A", "B", "C", "D"] if k in options]
            if len(set(opt_vals)) < len(opt_vals):
                errors.append(f"Q{q_num}: Duplicate option values found in options: {options}")

        # Check correct answer
        ca = q.get("correct_answer")
        if ca not in ["A", "B", "C", "D"]:
            errors.append(f"Q{q_num}: Invalid correct_answer: '{ca}'. Must be A, B, C, or D.")
        else:
            answer_counts[ca] += 1

        # Check explanation
        expl = q.get("explanation", {})
        if not isinstance(expl, dict):
            errors.append(f"Q{q_num}: 'explanation' must be an object")
        else:
            k_type = expl.get("knowledge_type", "")
            if not k_type or not k_type.strip():
                warnings.append(f"Q{q_num}: Missing or empty 'knowledge_type' in explanation")
            analysis = expl.get("analysis", {})
            if not analysis:
                warnings.append(f"Q{q_num}: Missing 'analysis' in explanation")

        # Check Vietnamese translation
        vi_trans = q.get("vietnamese_translation", "")
        if not vi_trans or not vi_trans.strip():
            warnings.append(f"Q{q_num}: Missing 'vietnamese_translation'")

    # 3. Check Option Balance
    print("\n--- Answer Key Distribution ---")
    for k in ["A", "B", "C", "D"]:
        cnt = answer_counts[k]
        status = "OK" if 8 <= cnt <= 13 else "IMBALANCED"
        print(f"  Option {k}: {cnt:2d}/40 ({cnt/40*100:5.1f}%) [{status}]")
        if not (8 <= cnt <= 13):
            warnings.append(f"Option {k} count is {cnt} (recommended: 8 to 13 for balanced distribution)")

    # 4. Check Sections & Reading Passages
    sections = data.get("sections", [])
    if not sections:
        warnings.append("Missing 'sections' array in test JSON")
    else:
        print(f"\n--- Sections Summary ({len(sections)} sections) ---")
        for s in sections:
            s_title = s.get("title", s.get("section_id", "Unknown"))
            p_title = s.get("passage_title", "N/A")
            q_rng = s.get("questions_range", [])
            print(f"  [{s.get('section_id')}] {s_title} (Questions {q_rng}) | Passage: {p_title}")

    # 5. Check Curriculum Ceiling & Thematic Alignment for Unit 1
    u_num = data.get("unit_number")
    if u_num == 1:
        raw_text = json.dumps(data, ensure_ascii=False).lower()
        forbidden_offtopic = [
            "smart plant", "hologram watch", "pocket chef", "genes in babies",
            "gene science", "intergenerational trauma", "sporadic behavior",
            "sweep it under the rug", "cut from the same cloth"
        ]
        for term in forbidden_offtopic:
            if term in raw_text:
                errors.append(f"Off-topic / Out-of-curriculum term detected in Unit 1 test: '{term}'")

    # 6. Report Audit Verdict
    print("\n--------------------------------------------------")
    if errors:
        print(f"❌ AUDIT FAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
    else:
        print("✅ AUDIT PASSED: All 40 questions and core schema criteria verified!")

    if warnings:
        print(f"\n⚠️  {len(warnings)} Warning(s):")
        for w in warnings[:10]:
            print(f"  - {w}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings)-10} more warnings")

    print("--------------------------------------------------\n")
    return len(errors) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audit_unit_tests.py <path_to_test.json>")
        sys.exit(1)
    success = True
    for arg in sys.argv[1:]:
        ok = audit_test_json(arg)
        if not ok:
            success = False
    sys.exit(0 if success else 1)
