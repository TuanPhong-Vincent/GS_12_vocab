import os
import sys
import glob
import json

def extract_sentences_from_json(filepath):
    filename = os.path.basename(filepath)
    output_lines = [f"=== FILE: {filename} ==="]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        output_lines.append(f"Error reading file: {e}")
        return "\n".join(output_lines)
    
    # 1. Multiple Choice / Error Identification / Sentence Building / Verb Form / Rewriting / Ordering / Signs
    if "questions" in data and isinstance(data["questions"], list):
        for q in data["questions"]:
            qid = q.get("id", "")
            text = q.get("text", "")
            ans = q.get("correct_answer", "")
            orig = q.get("original", "")
            base = q.get("base_word", "")
            words = q.get("words", [])
            sentences = q.get("sentences", [])
            vietnamese = q.get("vietnamese", "")
            sign_text = q.get("sign_text", "")
            q_text = q.get("question", "")
            
            line_parts = [f"[{filename} - Q{qid}]"]
            if orig:
                line_parts.append(f"Original: {orig}")
            if text:
                line_parts.append(f"Text: {text}")
            if vietnamese:
                line_parts.append(f"Vietnamese: {vietnamese}")
            if sentences:
                line_parts.append(f"Sentences: {' || '.join(sentences)}")
            if sign_text:
                line_parts.append(f"Sign/Notice: {sign_text}")
            if q_text and q_text != text:
                line_parts.append(f"Question: {q_text}")
            if words:
                line_parts.append(f"Words: {' / '.join(words)}")
            if base:
                line_parts.append(f"Base: {base}")
            if ans:
                line_parts.append(f"Ans: {ans}")
            output_lines.append(" | ".join(line_parts))

    # 2. Dictionary Entries
    elif "entries" in data and isinstance(data["entries"], list):
        for entry in data["entries"]:
            eid = entry.get("id", "")
            word = entry.get("word", "")
            bullets = entry.get("bullet_points", [])
            eqs = entry.get("questions", [])
            for b in bullets:
                output_lines.append(f"[{filename} - Entry {eid} ({word}) Bullet] {b}")
            for q in eqs:
                output_lines.append(f"[{filename} - Entry {eid} Q{q.get('id','')}] Text: {q.get('text','')} | Ans: {q.get('correct_answer','')}")

    # 3. Matching
    elif "pairs" in data and isinstance(data["pairs"], list):
        for p in data["pairs"]:
            pid = p.get("id", "")
            col_a = p.get("column_a", "")
            col_b = p.get("column_b", "")
            output_lines.append(f"[{filename} - Pair {pid}] {col_a} --- {col_b}")

    # 4. Paragraph Fill
    elif "paragraph_parts" in data and isinstance(data["paragraph_parts"], list):
        combined_text = []
        for part in data["paragraph_parts"]:
            if isinstance(part, str):
                combined_text.append(part)
            elif isinstance(part, dict):
                blank_id = part.get("id", "")
                blank_ans = part.get("correct_answer", "")
                combined_text.append(f"[Blank {blank_id}: {blank_ans}]")
        output_lines.append(f"[{filename} - Passage] " + "".join(combined_text))

    return "\n".join(output_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 prepare_context_text.py <target_directory_path> [output_file]")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: Directory not found: {target_dir}")
        sys.exit(1)
        
    json_files = sorted(glob.glob(os.path.join(target_dir, "*.json")))
    if not json_files:
        print(f"No .json files found in {target_dir}")
        sys.exit(1)
        
    all_content = []
    for jf in json_files:
        all_content.append(extract_sentences_from_json(jf))
        all_content.append("\n" + "="*50 + "\n")
        
    result_text = "\n".join(all_content)
    
    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result_text)
        print(f"Successfully exported {len(json_files)} files to {out_path}")
    else:
        print(result_text)

if __name__ == "__main__":
    main()
