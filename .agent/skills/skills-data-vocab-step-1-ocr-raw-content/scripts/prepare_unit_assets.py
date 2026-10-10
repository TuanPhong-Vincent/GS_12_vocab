"""One-click asset preparation for GS10 raw-content extraction.
Prepares both:
1. Scanned page images for Student's Book, Teacher's Book, and Workbook.
2. Digital text draft markdown for Tài liệu tập huấn and PTNL.
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
    from page_mapping import get_unit_mapping, print_unit_info
    from pdf2images import extract_unit_scanned_books
    from extract_digital_text import extract_digital_sources_for_unit
except ImportError:
    from .page_mapping import get_unit_mapping, print_unit_info
    from .pdf2images import extract_unit_scanned_books
    from .extract_digital_text import extract_digital_sources_for_unit

def prepare_all_unit_assets(unit_num: int, output_dir: str, workspace_root: str = ".", dpi: int = 150):
    mapping = get_unit_mapping(unit_num)
    print("=" * 60)
    print(f"PREPARING ASSETS FOR UNIT {unit_num}: {mapping['title'].upper()}")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)
    pages_dir = os.path.join(output_dir, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    # 1. Scanned PDFs -> Images
    print("\n[Phase 1] Extracting scanned pages (SB, TB, WB) to images...")
    extract_unit_scanned_books(unit_num, output_dir, workspace_root=workspace_root, dpi=dpi)

    # 2. Digital PDFs -> Text
    print("\n[Phase 2] Extracting digital text (TLTH, PTNL)...")
    extract_digital_sources_for_unit(unit_num, output_dir, workspace_root=workspace_root)

    # 3. Create instruction guide inside pages
    manifest_path = os.path.join(pages_dir, "TRANSCRIBE_GUIDE.md")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(f"# Transcription Guide for Unit {unit_num}: {mapping['title']}\n\n")
        f.write("Follow these steps to produce `raw-content.md`:\n\n")
        f.write("### 1. Student's Book (`pages/1_student_book/`)\n")
        f.write(f"- Pages: {mapping['sb']['start']} to {mapping['sb']['end']}\n")
        f.write("- Use `view_file` on each image to transcribe Getting Started, Language, Reading, Speaking, Listening, Writing, Communication/Culture, Looking Back, Project.\n\n")
        f.write("### 2. Teacher's Book (`pages/2_teacher_book/`)\n")
        f.write(f"- Pages: {mapping['tb']['start']} to {mapping['tb']['end']}\n")
        f.write("- Use `view_file` on each image to transcribe Objectives, Teacher notes, Audio scripts, and Official Answer Keys.\n\n")
        f.write("### 3. Workbook (`pages/3_workbook/`)\n")
        f.write(f"- Exercises: Pages {mapping['wb']['exercises']['start']} to {mapping['wb']['exercises']['end']}\n")
        f.write(f"- Answer Key: Pages {mapping['wb']['key']['start']} to {mapping['wb']['key']['end']}\n")
        f.write("- Use `view_file` to transcribe workbook exercises and answer keys.\n\n")
        f.write("### 4. Tài liệu tập huấn (`pages/4_tlth_digital.md`)\n")
        f.write("- Review and refine the already extracted digital text.\n\n")
        f.write("### 5. Phát triển năng lực (`pages/5_ptnl_digital.md`)\n")
        f.write("- Review and format the already extracted digital exercises and answer key.\n\n")
        f.write("### 6. Assembly\n")
        f.write("Assemble all 5 parts into `<Save Location>/raw-content.md` and then delete the `pages/` directory.\n")

    print(f"\n[Phase 3] Transcription guide written to '{manifest_path}'")
    print("=" * 60)
    print("Asset preparation complete! Proceed with agent multimodal transcription.")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare all source assets for a GS10 Unit")
    parser.add_argument("--unit", type=int, required=True, help="Unit number (1-10)")
    parser.add_argument("--output", required=True, help="Save location (e.g. lessons/unit-1/vocab)")
    parser.add_argument("--workspace", default=".", help="Root directory containing the 5 PDF files")
    parser.add_argument("--dpi", type=int, default=150, help="Image DPI (default: 150)")
    args = parser.parse_args()

    prepare_all_unit_assets(args.unit, args.output, workspace_root=args.workspace, dpi=args.dpi)
