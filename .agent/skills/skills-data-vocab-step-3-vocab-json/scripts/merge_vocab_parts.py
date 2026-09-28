#!/usr/bin/env python3
"""
Merge per-group vocab part files into a single vocab.json and clean up.

Usage:
    python3 merge_vocab_parts.py <target_directory>

The target directory should contain a `vocab/` subfolder with files named
`vocab-part-1.json`, `vocab-part-2.json`, ... — one per vocabulary group.

The script:
    - sorts the part files by their numeric suffix,
    - assigns sequential string `id`s to groups (1, 2, 3, ...) and to words
      (a single running counter across all groups),
    - writes the merged result to `vocab/vocab.json`,
    - deletes the part files.
"""

import glob
import json
import os
import sys
from pathlib import Path


def merge(target_dir: Path) -> None:
    vocab_dir = target_dir / "vocab"
    if not vocab_dir.is_dir():
        print(f"Error: {vocab_dir} does not exist.", file=sys.stderr)
        sys.exit(1)

    parts = sorted(
        glob.glob(str(vocab_dir / "vocab-part-*.json")),
        key=lambda x: int(Path(x).stem.split("-")[-1]),
    )
    if not parts:
        print(f"Error: no vocab-part-*.json files in {vocab_dir}.", file=sys.stderr)
        sys.exit(1)

    merged = []
    group_id = 1
    word_id = 1

    for p in parts:
        with open(p, encoding="utf-8") as f:
            group_data = json.load(f)

        new_group = {"id": str(group_id)}
        for k, v in group_data.items():
            if k != "id":
                new_group[k] = v

        for i, word in enumerate(new_group.get("words", [])):
            new_word = {"id": str(word_id)}
            for k, v in word.items():
                if k != "id":
                    new_word[k] = v
            new_group["words"][i] = new_word
            word_id += 1

        merged.append(new_group)
        group_id += 1

    output_path = vocab_dir / "vocab.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    for p in parts:
        os.remove(p)

    print(
        f"Merged {len(parts)} parts into {output_path} and cleaned up part files."
    )


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 merge_vocab_parts.py <target_directory>", file=sys.stderr)
        sys.exit(1)

    target_dir = Path(sys.argv[1]).resolve()
    if not target_dir.is_dir():
        print(f"Error: {target_dir} is not a directory.", file=sys.stderr)
        sys.exit(1)

    merge(target_dir)


if __name__ == "__main__":
    main()
