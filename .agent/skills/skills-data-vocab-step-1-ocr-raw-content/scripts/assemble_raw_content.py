"""Assemble the 5 source sections into a single, cohesive raw-content.md for a Unit.
Validates headers and content completeness.
"""

import sys
import os
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from page_mapping import get_unit_mapping
except ImportError:
    from .page_mapping import get_unit_mapping

def assemble_raw_content(unit_num: int, target_dir: str) -> str:
    mapping = get_unit_mapping(unit_num)
    pages_dir = os.path.join(target_dir, "pages")
    output_file = os.path.join(target_dir, "raw-content.md")

    # Header
    assembled = [
        f"# UNIT {unit_num}: {mapping['title'].upper()}",
        f"",
        f"> **Tài liệu nguồn tổng hợp Global Success 10 - Unit {unit_num}**",
        f"> - **1. Student's Book (GS10.pdf)**: Trang {mapping['sb']['start']} - {mapping['sb']['end']}",
        f"> - **2. Teacher's Book (GS10_TB.pdf)**: Trang {mapping['tb']['start']} - {mapping['tb']['end']}",
        f"> - **3. Workbook (GS10_WB.pdf)**: Bài tập trang {mapping['wb']['exercises']['start']} - {mapping['wb']['exercises']['end']} | Đáp án trang {mapping['wb']['key']['start']} - {mapping['wb']['key']['end']}",
        f"> - **4. Tài liệu tập huấn (GS10_Tailieutaphuan.pdf)**: Ma trận trang {mapping['tlth']['book_map']}, Phân phối trang {mapping['tlth']['distribution']}",
        f"> - **5. Bài tập Phát triển năng lực (GS10_PTNL.pdf)**: Bài tập trang {mapping['ptnl']['exercises']['start']} - {mapping['ptnl']['exercises']['end']} | Đáp án trang {mapping['ptnl']['key']['start']} - {mapping['ptnl']['key']['end']}",
        f"",
        f"---",
        f""
    ]

    # Source files mapping to search in pages/
    sources = [
        ("1. Student's Book (GS10.pdf)", ["1_sb.md", "1_student_book.md", "sb.md"]),
        ("2. Teacher's Book (GS10_TB.pdf)", ["2_tb.md", "2_teacher_book.md", "tb.md"]),
        ("3. Workbook (GS10_WB.pdf)", ["3_wb.md", "3_workbook.md", "wb.md"]),
        ("4. Tài liệu tập huấn (GS10_Tailieutaphuan.pdf)", ["4_tlth_digital.md", "4_tlth.md", "tlth.md"]),
        ("5. Bài tập Phát triển năng lực (GS10_PTNL.pdf)", ["5_ptnl_digital.md", "5_ptnl.md", "ptnl.md"]),
    ]

    missing = []
    for label, candidate_names in sources:
        found_content = None
        for name in candidate_names:
            candidate_path = os.path.join(pages_dir, name)
            if os.path.isfile(candidate_path):
                with open(candidate_path, "r", encoding="utf-8") as f:
                    found_content = f.read().strip()
                break

        if found_content:
            # Ensure top header matches if not present
            if not found_content.startswith("## "):
                assembled.append(f"## {label}\n")
            assembled.append(found_content)
            assembled.append("\n---\n")
        else:
            missing.append(label)

    if missing:
        print(f"Note: Some source files were not found in '{pages_dir}': {', '.join(missing)}")

    content_str = "\n".join(assembled)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content_str)

    print(f"Successfully assembled 'raw-content.md' at '{output_file}' ({len(content_str.splitlines())} lines).")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assemble raw-content.md from individual unit parts")
    parser.add_argument("--unit", type=int, required=True, help="Unit number (1-10)")
    parser.add_argument("--dir", required=True, help="Target directory (containing pages/ and where raw-content.md should be written)")
    args = parser.parse_args()

    assemble_raw_content(args.unit, args.dir)
