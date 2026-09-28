#!/usr/bin/env python3
"""
Vocabulary Coverage Checker
Checks how many vocabulary words from vocab.json are used in HTML and JSON exercise files within a folder.

Usage:
    python vocab_coverage_checker.py <vocab_json_path> <folder_path>

Example:
    python vocab_coverage_checker.py "book-writing/Unit 1/vocab.json" "book-writing/Unit 1/A. Vocabulary"
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import argparse
try:
    from lemminflect import getAllInflections
except ImportError:
    getAllInflections = None

class VocabularyCoverageChecker:
    def __init__(self, vocab_json_path: str, folder_path: str):
        self.folder_path = Path(folder_path)
        self.vocab_json_path = Path(vocab_json_path)
        self.vocab_data = {}
        self.used_words = set()
        self.unused_words = set()
        self.word_groups = {}

    def load_vocabulary(self) -> bool:
        """Load vocabulary data from JSON file."""
        try:
            with open(self.vocab_json_path, 'r', encoding='utf-8') as f:
                self.vocab_data = json.load(f)
            return True
        except FileNotFoundError:
            print(f"❌ Error: Vocabulary file not found: {self.vocab_json_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in vocabulary file: {e}")
            return False

    def extract_all_words(self) -> Dict[str, List[str]]:
        """Extract all vocabulary words grouped by category."""
        all_words = {}

        for group in self.vocab_data:
            group_name = group.get('group', 'Unknown')
            words = []

            for word_data in group.get('words', []):
                english_word = word_data.get('english_word', '')
                if english_word:
                    words.append(english_word)

            all_words[group_name] = words
            self.word_groups[group_name] = words

        return all_words

    def find_exercise_files(self) -> List[Path]:
        """Find all HTML and JSON exercise files in the specified folder."""
        files = []

        if not self.folder_path.exists():
            print(f"❌ Error: Folder not found: {self.folder_path}")
            return files

        for ext in ["*.html", "*.json"]:
            files.extend(self.folder_path.rglob(ext))

        # Filter out vocab.json itself if it happens to be in the folder
        return [f for f in files if f.name != "vocab.json"]

    def combine_file_contents(self, files: List[Path]) -> str:
        """Combine all file contents into a single string, handling both HTML and JSON."""
        combined_content = ""
        for file_path in files:
            try:
                if file_path.suffix == '.json':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        def extract_strings(obj):
                            strings = []
                            if isinstance(obj, dict):
                                for v in obj.values():
                                    strings.extend(extract_strings(v))
                            elif isinstance(obj, list):
                                for item in obj:
                                    strings.extend(extract_strings(item))
                            elif isinstance(obj, str):
                                strings.append(obj)
                            return strings
                        
                        extracted = extract_strings(data)
                        combined_content += " ".join(extracted) + "\n"
                elif file_path.suffix == '.html':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Remove HTML comments
                        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
                        
                        # Remove alt text from img tags
                        content = re.sub(r'alt="[^"]*"', '', content)
                        
                        # Remove title attributes
                        content = re.sub(r'title="[^"]*"', '', content)
                        
                        combined_content += content + "\n"
            except Exception as e:
                print(f"⚠️  Warning: Could not read file {file_path}: {e}")
        return combined_content

    def extract_words_from_combined_html(self, combined_content: str) -> Dict[str, int]:
        """Extract vocabulary words from the combined HTML content with occurrence counts."""
        words_found = {}  # Store counts for ALL words, not just >= 3
        content_lower = combined_content.lower()

        for group_name, words in self.word_groups.items():
            for word in words:
                word_lower = word.lower()
                count = 0
                
                # Check for exact word match first
                pattern = rf'\b{re.escape(word_lower)}\b'
                matches = re.findall(pattern, content_lower)
                count += len(matches)
                
                # Only check for variations if no exact matches found
                # This prevents double counting
                if count == 0:
                    variations = self._get_all_word_variations(word_lower)
                    for var in variations:
                        if not var: continue
                        var_pattern = rf'\b{re.escape(var)}\b'
                        matches = re.findall(var_pattern, content_lower)
                        count += len(matches)
                
                # Store count for ALL words (even 0)
                words_found[word] = count
        
        return words_found

    def _get_all_word_variations(self, word: str) -> Set[str]:
        """Get all morphological variations of a word (nouns and verbs)."""
        variations = set()
        
        # If there are slashes, add versions for each alternative: "pants / trousers" -> "pants", "trousers"
        if "/" in word:
            for part in [p.strip() for p in word.split("/")]:
                if part:
                    variations.add(part)
                    if part.endswith("'s"):
                        variations.add(part[:-2])
                    variations.update(self._get_all_word_variations(part))
        
        # If there are parentheses, add versions with/without parenthesized words
        if "(" in word and ")" in word:
            # Version without parentheses: "wash (your) face" -> "wash your face"
            clean_with_parens_content = word.replace("(", "").replace(")", "")
            variations.add(clean_with_parens_content)
            # If the parenthesized word is "your", also support other possessives
            if "your" in clean_with_parens_content:
                for pos in ["our", "my", "his", "her", "their"]:
                    variations.add(clean_with_parens_content.replace("your", pos))
            # Also add morphological variations of this version
            variations.update(self._get_all_word_variations(clean_with_parens_content))
            
            # Version without the parenthesized part entirely: "wash (your) face" -> "wash face"
            clean_without_parens_content = re.sub(r'\s*\([^)]*\)\s*', ' ', word).strip()
            clean_without_parens_content = re.sub(r'\s+', ' ', clean_without_parens_content)
            variations.add(clean_without_parens_content)
            variations.update(self._get_all_word_variations(clean_without_parens_content))
            
        # Try with lemminflect if available
        if getAllInflections is not None:
            # Try as noun
            noun_inflections = getAllInflections(word, upos='NOUN')
            if noun_inflections:
                for tag, forms in noun_inflections.items():
                    variations.update(forms)
                    
            # Try as verb
            verb_inflections = getAllInflections(word, upos='VERB')
            if verb_inflections:
                for tag, forms in verb_inflections.items():
                    variations.update(forms)
                    
            # Handle phrasal verbs or multi-word terms
            if " " in word:
                parts = word.split(" ", 1)
                first_word = parts[0]
                rest = parts[1]
                
                first_word_verbs = getAllInflections(first_word, upos='VERB')
                if first_word_verbs:
                    for tag, forms in first_word_verbs.items():
                        for f in forms:
                            variations.add(f"{f} {rest}")
                            
                parts_last = word.rsplit(" ", 1)
                first_part = parts_last[0]
                last_word = parts_last[1]
                last_word_nouns = getAllInflections(last_word, upos='NOUN')
                if last_word_nouns:
                    for tag, forms in last_word_nouns.items():
                        for f in forms:
                            variations.add(f"{first_part} {f}")
                        
        # Basic heuristic fallbacks
        if not word.endswith('s'):
            variations.update([f"{word}s", f"{word}es"])
        else:
            variations.add(word[:-1])
            if word.endswith('es'):
                variations.add(word[:-2])
                
        base_word = word
        if word.endswith('ing'): base_word = word[:-3]
        elif word.endswith('ed'): base_word = word[:-2]
        elif word.endswith('er'): base_word = word[:-2]
        elif word.endswith('est'): base_word = word[:-3]
        
        if base_word != word:
            variations.update([
                base_word,
                f"{base_word}ing",
                f"{base_word}ed",
                f"{base_word}er",
                f"{base_word}est",
                f"{base_word}s"
            ])
            
        # Ensure exact original word is not included in the variation list 
        # (since exact matches are checked first separately)
        if word in variations:
            variations.remove(word)
            
        return variations

    def analyze_coverage(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]], Dict[str, int]]:
        """Analyze vocabulary coverage across all exercise files."""
        exercise_files = self.find_exercise_files()

        if not exercise_files:
            print("❌ No HTML or JSON exercise files found in the specified folder.")
            return {}, {}, {}

        print(f"📁 Found {len(exercise_files)} exercise files in {self.folder_path}")

        # Combine all contents into one string
        combined_content = self.combine_file_contents(exercise_files)

        # Find all used words in the combined content with counts
        all_words_with_counts = self.extract_words_from_combined_html(combined_content)

        print(f"🔎 Scanned all exercise files. Found occurrence counts for all vocabulary words.")

        # Categorize words by usage (used = any occurrence, unused = 0 occurrences)
        used_by_group = {}
        unused_by_group = {}

        for group_name, words in self.word_groups.items():
            used_words = [word for word in words if all_words_with_counts.get(word, 0) > 0]
            unused_words = [word for word in words if all_words_with_counts.get(word, 0) == 0]

            used_by_group[group_name] = used_words
            unused_by_group[group_name] = unused_words

        self.used_words = set()
        for words in used_by_group.values():
            self.used_words.update(words)
            
        self.unused_words = set()
        for words in unused_by_group.values():
            self.unused_words.update(words)

        return used_by_group, unused_by_group, all_words_with_counts

    def generate_report(self, used_by_group: Dict[str, List[str]],
                       unused_by_group: Dict[str, List[str]], 
                       word_counts: Dict[str, int]) -> None:
        """Generate a detailed coverage report."""
        total_words = sum(len(words) for words in self.word_groups.values())
        total_used = len(self.used_words)
        total_unused = len(self.unused_words)
        coverage_percentage = (total_used / total_words) * 100 if total_words > 0 else 0

        print("\n" + "="*80)
        print("📊 VOCABULARY COVERAGE REPORT")
        print("="*80)
        print(f"📈 Overall Coverage: {total_used}/{total_words} words ({coverage_percentage:.1f}%)")
        print(f"✅ Used words (any occurrence): {total_used}")
        print(f"❌ Unused words (0 occurrences): {total_unused}")
        print()

        # Detailed breakdown by group
        print("📋 DETAILED BREAKDOWN BY GROUP:")
        print("-" * 80)

        for group_name in sorted(self.word_groups.keys()):
            used_count = len(used_by_group.get(group_name, []))
            total_count = len(self.word_groups[group_name])
            group_coverage = (used_count / total_count) * 100 if total_count > 0 else 0

            status = "✅" if used_count == total_count else "⚠️" if used_count > 0 else "❌"
            print(f"{status} {group_name}: {used_count}/{total_count} ({group_coverage:.1f}%)")

            if used_by_group.get(group_name):
                used_words = used_by_group[group_name]
                print(f"    ✅ Used: {', '.join([f'{word}({word_counts[word]})' for word in used_words])}")
            
            if unused_by_group.get(group_name):
                unused_words = unused_by_group[group_name]
                print(f"    ❌ Unused: {', '.join(unused_words)}")
            print()

        # Summary of unused words
        if self.unused_words:
            print("🔍 UNUSED WORDS SUMMARY:")
            print("-" * 80)
            unused_list = sorted(list(self.unused_words))
            for i, word in enumerate(unused_list, 1):
                print(f"{i:2d}. {word}")

        # Word frequency summary (only words with > 0 occurrences)
        used_words_with_counts = {word: count for word, count in word_counts.items() if count > 0}
        if used_words_with_counts:
            print("\n📊 WORD FREQUENCY SUMMARY (used words only):")
            print("-" * 80)
            sorted_words = sorted(used_words_with_counts.items(), key=lambda x: x[1], reverse=True)
            for i, (word, count) in enumerate(sorted_words, 1):
                print(f"{i:2d}. {word}: {count} times")

        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 80)
        if coverage_percentage < 50:
            print("⚠️  Low coverage detected! Consider adding more vocabulary exercises.")
        elif coverage_percentage < 80:
            print("📝 Moderate coverage. Some important words are missing.")
        else:
            print("🎉 Excellent coverage! Most vocabulary is being used.")

        if self.unused_words:
            print(f"📝 Consider adding exercises for the {len(self.unused_words)} unused words.")
        
        # Frequency-based recommendations
        high_freq_words = [word for word, count in word_counts.items() if count >= 10]
        if high_freq_words:
            print(f"🎯 High-frequency words (>=10 times): {', '.join(high_freq_words[:5])}{'...' if len(high_freq_words) > 5 else ''}")
            print("💡 Consider reducing frequency of these words to balance the content.")

    def run(self) -> bool:
        """Run the complete vocabulary coverage analysis."""
        print("🔍 Vocabulary Coverage Checker")
        print("="*50)

        # Load vocabulary data
        if not self.load_vocabulary():
            return False

        # Extract all words
        all_words = self.extract_all_words()
        print(f"📚 Loaded {sum(len(words) for words in all_words.values())} vocabulary words from {len(all_words)} groups")

        # Analyze coverage
        used_by_group, unused_by_group, all_used_words_with_counts = self.analyze_coverage()

        # Generate report
        self.generate_report(used_by_group, unused_by_group, all_used_words_with_counts)

        return True

def main():
    parser = argparse.ArgumentParser(
        description="Check vocabulary coverage in HTML and JSON exercise files against vocab.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vocab_coverage_checker.py "book-writing/Unit 1/vocab.json" "book-writing/Unit 1/A. Vocabulary"
  python vocab_coverage_checker.py "./vocab.json" "./exercises"
        """
    )

    parser.add_argument(
        "vocab_json_path", 
        help="Path to the vocab.json file containing vocabulary data"
    )
    parser.add_argument(
        "folder_path",
        help="Path to the folder containing HTML files to analyze"
    )

    args = parser.parse_args()

    # Create checker and run analysis
    checker = VocabularyCoverageChecker(args.vocab_json_path, args.folder_path)
    success = checker.run()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 