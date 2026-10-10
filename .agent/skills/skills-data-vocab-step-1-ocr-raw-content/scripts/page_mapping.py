"""Master page mapping for Global Success 12 (GS12) from GS12.pdf.
All page numbers are 1-indexed (matching PDF viewer and fitz 1-based page indexing).
"""

import sys
import json
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Master mapping for Units 1 - 10 of Global Success 12 (GS12.pdf)
UNIT_MAPPING = {
    1: {
        "unit": 1,
        "title": "Life Stories We Admire",
        "theme": "Life stories, biographies, personal accounts, national heroes",
        "grammar": "Past simple vs. Past continuous",
        "pronunciation": "Diphthongs /eɪ/ and /əʊ/",
        "sb": {"start": 8, "end": 19, "desc": "Getting Started to Project"},
    },
    2: {
        "unit": 2,
        "title": "A Multicultural World",
        "theme": "Cultural diversity, traditions, world cuisines, festivals",
        "grammar": "Articles (review and extension)",
        "pronunciation": "Diphthongs /ɔɪ/, /aɪ/, and /aʊ/",
        "sb": {"start": 20, "end": 31, "desc": "Getting Started to Project"},
    },
    3: {
        "unit": 3,
        "title": "Green Living",
        "theme": "Eco-friendly lifestyle, reducing plastic waste, renewable energy",
        "grammar": "Verbs with prepositions; Relative clauses referring to a whole sentence",
        "pronunciation": "Diphthongs /ɪə/, /eə/, and /ʊə/",
        "sb": {"start": 32, "end": 43, "desc": "Getting Started to Project"},
    },
    "review_1": {
        "unit": "review_1",
        "title": "Review 1 (Units 1 - 3)",
        "sb": {"start": 44, "end": 47, "desc": "Language and Skills Review 1"},
    },
    4: {
        "unit": 4,
        "title": "Urbanisation",
        "theme": "Urban growth, city infrastructure, rural-to-urban migration",
        "grammar": "Present perfect (review and extension); Double comparatives to show change",
        "pronunciation": "Unstressed words in connected speech",
        "sb": {"start": 48, "end": 59, "desc": "Getting Started to Project"},
    },
    5: {
        "unit": 5,
        "title": "The World of Work",
        "theme": "Workplace skills, job applications, modern career expectations",
        "grammar": "Simple, compound, and complex sentences (review and extension)",
        "pronunciation": "Stressing auxiliary and modal verbs",
        "sb": {"start": 60, "end": 71, "desc": "Getting Started to Project"},
    },
    "review_2": {
        "unit": "review_2",
        "title": "Review 2 (Units 4 - 5)",
        "sb": {"start": 72, "end": 75, "desc": "Language and Skills Review 2"},
    },
    6: {
        "unit": 6,
        "title": "Artificial Intelligence",
        "theme": "AI technology, automation, robotics, ethical considerations",
        "grammar": "Active and passive causatives",
        "pronunciation": "Homophones",
        "sb": {"start": 76, "end": 87, "desc": "Getting Started to Project"},
    },
    7: {
        "unit": 7,
        "title": "The World of Mass Media",
        "theme": "Social networks, journalism, digital broadcasting, fake news",
        "grammar": "Adverbial clauses of manner and result",
        "pronunciation": "Linking /r/ between two vowels",
        "sb": {"start": 88, "end": 99, "desc": "Getting Started to Project"},
    },
    8: {
        "unit": 8,
        "title": "Wildlife Conservation",
        "theme": "Endangered species, biodiversity protection, national parks",
        "grammar": "Adverbial clauses of condition and comparison",
        "pronunciation": "Assimilation",
        "sb": {"start": 100, "end": 111, "desc": "Getting Started to Project"},
    },
    "review_3": {
        "unit": "review_3",
        "title": "Review 3 (Units 6 - 8)",
        "sb": {"start": 112, "end": 115, "desc": "Language and Skills Review 3"},
    },
    9: {
        "unit": 9,
        "title": "Career Paths",
        "theme": "Choosing future vocations, higher education vs apprenticeships",
        "grammar": "Three-word phrasal verbs",
        "pronunciation": "Sentence stress and rhythm",
        "sb": {"start": 116, "end": 127, "desc": "Getting Started to Project"},
    },
    10: {
        "unit": 10,
        "title": "Lifelong Learning",
        "theme": "Continuous self-improvement, adult education, digital learning",
        "grammar": "Reported speech: reporting orders, requests, offers, and advice",
        "pronunciation": "Intonation in questions (revision)",
        "sb": {"start": 128, "end": 139, "desc": "Getting Started to Project"},
    },
    "review_4": {
        "unit": "review_4",
        "title": "Review 4 (Units 9 - 10)",
        "sb": {"start": 138, "end": 141, "desc": "Language and Skills Review 4"},
    },
    "glossary": {
        "unit": "glossary",
        "title": "Glossary / Wordlist",
        "sb": {"start": 142, "end": 155, "desc": "Alphabetical vocabulary glossary for GS12"},
    }
}

def get_unit_mapping(unit_num):
    """Retrieve mapping dict for given unit number (1-10) or string key."""
    if isinstance(unit_num, str) and unit_num.isdigit():
        unit_num = int(unit_num)
    return UNIT_MAPPING.get(unit_num, None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query page mapping for GS12 units")
    parser.add_argument("--unit", type=int, help="Unit number (1-10)")
    parser.add_argument("--all", action="store_true", help="Dump all mappings as JSON")
    args = parser.parse_args()

    if args.all:
        print(json.dumps(UNIT_MAPPING, indent=2, ensure_ascii=False))
    elif args.unit:
        m = get_unit_mapping(args.unit)
        if m:
            print(json.dumps(m, indent=2, ensure_ascii=False))
        else:
            print(f"Unit {args.unit} not found in GS12 mapping.", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
