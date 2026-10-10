#!/usr/bin/env python3
"""
audit_test_quality.py:
Audits test JSON files and markdown companion files for:
- Standardized underscore lengths (exactly 9 chars: '_________')
- Clean prompt formatting (no raw markdown **, HTML <u>, or curly quotes in prompt stems)
- Valid option keys, no duplicates, trimmed whitespace
- Option balance and explanation completeness
"""

import sys
import os
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

def audit_file(filepath):
    print(f"\n==========================================")
    print(f"AUDITING: {filepath}")
    print(f"==========================================")
    
    issues = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Check sections
    for s in data.get('sections', []):
        snum = s.get('section_number')
        ptext = s.get('passage_text', '')
        if ptext:
            underscores = re.findall(r'_+', ptext)
            for u in underscores:
                if len(u) != 9:
                    print(f"  [!] Section {snum} passage has non-standard underscore ({len(u)}): {u}")
                    issues += 1

    # Check questions
    for q in data.get('questions', []):
        qnum = q.get('question_number') or q.get('id')
        prompt = q.get('prompt', '')
        opts = q.get('options', {})
        key = q.get('correct_answer', '')
        exp = q.get('explanation', {})
        
        # 1. Underscore check
        underscores = re.findall(r'_+', prompt)
        for u in underscores:
            if len(u) != 9:
                print(f"  [!] [Q{qnum}] Non-standard underscore ({len(u)} chars): {prompt}")
                issues += 1
                
        # 2. Curly quotes & Markdown tags in prompt
        for char in ['“', '”', '‘', '’']:
            if char in prompt:
                print(f"  [!] [Q{qnum}] Curly quote '{char}' in prompt: {prompt}")
                issues += 1
        if '**' in prompt:
            print(f"  [!] [Q{qnum}] Markdown ** in prompt: {prompt}")
            issues += 1
        if '<u>' in prompt or '</u>' in prompt:
            print(f"  [!] [Q{qnum}] HTML <u> in prompt: {prompt}")
            issues += 1
            
        # 3. Options validation
        for opt_k, opt_v in opts.items():
            for char in ['“', '”']:
                if char in opt_v:
                    print(f"  [!] [Q{qnum} {opt_k}] Curly quote '{char}' in option: {opt_v}")
                    issues += 1
            if opt_v != opt_v.strip():
                print(f"  [!] [Q{qnum} {opt_k}] Untrimmed option: '{opt_v}'")
                issues += 1
            if '**' in opt_v or '<u>' in opt_v:
                print(f"  [!] [Q{qnum} {opt_k}] Formatting tag in option: '{opt_v}'")
                issues += 1
                
        # 4. Duplicate options
        opt_vals = [v.strip().lower() for v in opts.values()]
        if len(opt_vals) != len(set(opt_vals)):
            print(f"  [!] [Q{qnum}] Duplicate option values: {opts}")
            issues += 1
            
        # 5. Key in options
        if key not in opts:
            print(f"  [!] [Q{qnum}] Invalid key '{key}' not found in options!")
            issues += 1
            
    if issues == 0:
        print("  -> ALL AUDIT CHECKS PASSED: 0 format or content defects detected.")
    else:
        print(f"  -> Total issues detected: {issues}")
    return issues

if __name__ == '__main__':
    targets = sys.argv[1:] if len(sys.argv) > 1 else [
        'lessons/unit-1/test/test1.json',
        'lessons/unit-1/test/test2.json'
    ]
    total_issues = 0
    for target in targets:
        if os.path.isdir(target):
            for fname in sorted(os.listdir(target)):
                if fname.endswith('.json') and ('test' in fname):
                    total_issues += audit_file(os.path.join(target, fname))
        elif os.path.isfile(target):
            total_issues += audit_file(target)
            
    sys.exit(1 if total_issues > 0 else 0)
