"""Extract digital text from GS10_Tailieutaphuan.pdf and GS10_PTNL.pdf for a specified Unit.
These two PDFs contain native digital text layers, so verbatim extraction is fast, exact, and preserves original wording.
"""

import sys
import os
import argparse
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from page_mapping import get_unit_mapping
except ImportError:
    from .page_mapping import get_unit_mapping

def clean_page_text(text: str) -> str:
    """Normalize whitespace and formatting in extracted text."""
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Drop standalone footer page numbers
        if stripped.isdigit() and len(stripped) <= 3:
            continue
        cleaned_lines.append(line.rstrip())
    
    # Rejoin lines
    result = "\n".join(cleaned_lines)
    # Collapse 3+ newlines to 2
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()

def extract_ptnl_for_unit(unit_num: int, ptnl_pdf: str) -> str:
    """Extract exercises and answer key from GS10_PTNL.pdf for given unit."""
    import fitz
    mapping = get_unit_mapping(unit_num)
    doc = fitz.open(ptnl_pdf)

    # 1. Exercises
    ex_start = mapping["ptnl"]["exercises"]["start"]
    ex_end = mapping["ptnl"]["exercises"]["end"]
    
    ex_texts = []
    for p in range(ex_start - 1, ex_end):
        p_text = clean_page_text(doc[p].get_text())
        ex_texts.append(f"<!-- PTNL Page {p + 1} -->\n{p_text}")

    # 2. Answer key
    key_start = mapping["ptnl"]["key"]["start"]
    key_end = mapping["ptnl"]["key"]["end"]
    key_texts = []
    for p in range(key_start - 1, key_end):
        p_text = clean_page_text(doc[p].get_text())
        key_texts.append(f"<!-- PTNL Answer Key Page {p + 1} -->\n{p_text}")

    doc.close()

    content = f"## 5. Bài tập Phát triển năng lực (GS10_PTNL.pdf)\n\n"
    content += f"<!-- Source: GS10_PTNL.pdf | Exercises: pp. {ex_start}-{ex_end} | Answer Key: pp. {key_start}-{key_end} -->\n\n"
    content += f"### Bài tập Phát triển năng lực Unit {unit_num}: {mapping['title']}\n\n"
    content += "\n\n".join(ex_texts)
    content += f"\n\n### Đáp án (Answer Key) PTNL Unit {unit_num}\n\n"
    content += "\n\n".join(key_texts)
    return content

def extract_tlth_for_unit(unit_num: int, tlth_pdf: str) -> str:
    """Extract curriculum distribution, book map, and pedagogical guidelines from GS10_Tailieutaphuan.pdf."""
    import fitz
    mapping = get_unit_mapping(unit_num)
    doc = fitz.open(tlth_pdf)

    tlth_cfg = mapping["tlth"]
    sections = []

    # 1. Book Map info (typically pp. 11-12)
    book_map_pages = tlth_cfg.get("book_map", [11, 12])
    bm_text = []
    for pno in book_map_pages:
        txt = doc[pno - 1].get_text()
        # Find Unit block
        lines = txt.split("\n")
        unit_block = []
        capture = False
        target_unit_header = f"UNIT {unit_num}"
        for line in lines:
            l_up = line.strip().upper()
            if target_unit_header in l_up:
                capture = True
            elif capture and any(f"UNIT {u}" in l_up for u in range(1, 11) if u != unit_num):
                break
            if capture:
                unit_block.append(line.rstrip())
        if unit_block:
            bm_text.append("\n".join(unit_block))
    
    if bm_text:
        sections.append(f"### Ma trận chương trình (Book Map)\n<!-- Source: GS10_Tailieutaphuan.pdf (pp. {', '.join(map(str, book_map_pages))}) -->\n" + "\n".join(bm_text))

    # 2. Teaching distribution (Phân phối chương trình)
    dist_pages = tlth_cfg.get("distribution", [23])
    dist_lines = []
    for pno in dist_pages:
        txt = doc[pno - 1].get_text()
        for line in txt.split("\n"):
            l_up = line.strip().upper()
            if f"UNIT {unit_num}" in l_up or f"BÀI/UNIT" in l_up or "TUẦN" in l_up:
                dist_lines.append(line.rstrip())
    
    # Alternatively capture the table lines mentioning Unit
    raw_dist = []
    for pno in dist_pages:
        txt = doc[pno - 1].get_text()
        lines = txt.split("\n")
        for i, l in enumerate(lines):
            if f"UNIT {unit_num}" in l.upper():
                # Grab surrounding context
                start_i = max(0, i - 2)
                end_i = min(len(lines), i + 4)
                raw_dist.extend(lines[start_i:end_i])
    
    if raw_dist:
        dedup_dist = []
        for l in raw_dist:
            if l.strip() and l not in dedup_dist:
                dedup_dist.append(l.strip())
        sections.append(f"### Phân phối chương trình (Teaching Distribution)\n<!-- Source: GS10_Tailieutaphuan.pdf (pp. {', '.join(map(str, dist_pages))}) -->\n" + "\n".join(dedup_dist))

    # 3. Special illustrations / lesson plans if any
    ill_pages = tlth_cfg.get("illustrations", [])
    if ill_pages:
        ill_text = []
        for pno in ill_pages:
            txt = clean_page_text(doc[pno - 1].get_text())
            ill_text.append(f"<!-- Page {pno} -->\n{txt}")
        sections.append(f"### Hướng dẫn giảng dạy & Giáo án minh họa\n<!-- Source: GS10_Tailieutaphuan.pdf (pp. {ill_pages[0]}-{ill_pages[-1]}) -->\n" + "\n\n".join(ill_text))

    doc.close()

    content = f"## 4. Tài liệu tập huấn (GS10_Tailieutaphuan.pdf)\n\n"
    content += f"<!-- Source: GS10_Tailieutaphuan.pdf | {tlth_cfg['desc']} -->\n\n"
    content += "\n\n".join(sections)
    return content

def extract_digital_sources_for_unit(unit_num: int, output_base: str, workspace_root: str = "."):
    """Extract digital content for both GS10_PTNL.pdf and GS10_Tailieutaphuan.pdf."""
    pages_base = os.path.join(output_base, "pages")
    os.makedirs(pages_base, exist_ok=True)

    ptnl_pdf = os.path.join(workspace_root, "GS10_PTNL.pdf")
    tlth_pdf = os.path.join(workspace_root, "GS10_Tailieutaphuan.pdf")

    results = {}

    if os.path.isfile(tlth_pdf):
        tlth_content = extract_tlth_for_unit(unit_num, tlth_pdf)
        tlth_out_path = os.path.join(pages_base, "4_tlth_digital.md")
        with open(tlth_out_path, "w", encoding="utf-8") as f:
            f.write(tlth_content)
        results["tlth"] = tlth_out_path
        print(f"-> Tài liệu tập huấn: extracted digital markdown to '{tlth_out_path}'")
    else:
        print(f"Warning: {tlth_pdf} not found. Skipping TLTH.")

    if os.path.isfile(ptnl_pdf):
        ptnl_content = extract_ptnl_for_unit(unit_num, ptnl_pdf)
        ptnl_out_path = os.path.join(pages_base, "5_ptnl_digital.md")
        with open(ptnl_out_path, "w", encoding="utf-8") as f:
            f.write(ptnl_content)
        results["ptnl"] = ptnl_out_path
        print(f"-> Bài tập PTNL: extracted digital markdown to '{ptnl_out_path}'")
    else:
        print(f"Warning: {ptnl_pdf} not found. Skipping PTNL.")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract digital text for GS10_PTNL and GS10_Tailieutaphuan")
    parser.add_argument("--unit", type=int, required=True, help="GS10 Unit number (1-10)")
    parser.add_argument("--output", required=True, help="Output destination folder (e.g. lessons/unit-1/vocab)")
    parser.add_argument("--workspace", default=".", help="Root folder containing GS10 PDFs (default: .)")
    args = parser.parse_args()

    extract_digital_sources_for_unit(args.unit, args.output, workspace_root=args.workspace)
