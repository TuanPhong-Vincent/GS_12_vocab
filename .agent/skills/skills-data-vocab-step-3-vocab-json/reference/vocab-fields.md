# Vocab JSON Field Rules and Part-File Schema

Each vocabulary group is written to its own part file (`vocab/vocab-part-{N}.json`) and merged into `vocab/vocab.json` at the end. This document describes the per-word fields, the file shape, and the path conventions for media references.

## Part-file shape

A part file contains a single JSON object with a `group` name and a `words` array. The top-level `id` is added later by the merge script — do not assign it yourself.

```json
{
  "group": "Topic Name",
  "words": [
    {
      "english_word": "example word",
      "pronunciation_british": "/ɪgˈzɑːmpl wɜːd/",
      "pronunciation_american": "/ɪgˈzæmpl wɝːd/",
      "vietnamese_meaning": "(n): từ ví dụ",
      "example_sentence_en": "This is an example sentence.",
      "example_sentence_vi": "Đây là một câu ví dụ.",
      "audio_word": "/lessons/media/gs9/unit-1/audio/example-word.mp3",
      "audio_sentence": "/lessons/media/gs9/unit-1/audio/example-word-sentence.mp3",
      "image": "/lessons/media/gs9/unit-1/images/example-word.webp",
      "alt": "Image for example word"
    }
  ]
}
```

## Per-word fields

Each entry in `words` must include every field below. The values (meanings and context alignment) come from the source files (`raw-vocabulary.md` and `raw-content.md`), except for example sentences which must be newly written to avoid copyright issues.

- **`english_word`** — the word or phrase exactly as it appears in `raw-vocabulary.md`. Preserve capitalization (lowercase unless it is a proper noun) and any internal spaces.
- **`pronunciation_british`** — British English IPA. Do **not** include syllable divisions: write `/ˈkʌmpəs/`, not `/ˈkʌm.pəs/`. A syllable break in IPA causes the audio engine to read the word as two tokens.
- **`pronunciation_american`** — American English IPA. Same rule — no syllable divisions.
- **`vietnamese_meaning`** — the Vietnamese translation prefixed with the part-of-speech abbreviation, e.g. `(n): từ ví dụ`, `(v): làm gì đó`, `(adj): tính từ`, `(phr.v): cụm động từ`. If a word has several senses, pick the sense that matches how the word is actually used in `raw-content.md` (e.g. for "original techniques", the meaning is "existing since the beginning", not "creative/new").
- **`example_sentence_en`** — an original English example sentence. Due to copyright reasons, **do not copy sentences directly from `raw-content.md`**. Instead, write a completely new, original example sentence that uses the vocabulary word in a way that matches the lesson's context and level of difficulty, **and actively incorporates the target grammar structures specified in the Grammar section of `raw-content.md`** (e.g. relative clauses referring to a whole sentence, verbs with prepositions, specific tenses, conditionals, passive forms).
- **`example_sentence_vi`** — a faithful Vietnamese translation of `example_sentence_en`.
- **`audio_word`**, **`audio_sentence`**, **`image`**, **`alt`** — see [Media path conventions](#media-path-conventions) below.

## Media path conventions

All media paths are **absolute** and start with `/lessons/media/`. The remaining segments are derived from the target directory.

- `{book_slug}` — short code for the book series. `global-success-9` → `gs9`, `global-success-6` → `gs6`, etc.
- `{unit_slug}` — the unit folder name in lowercase with hyphens, e.g. `Unit 1` → `unit-1`.
- `{word-with-hyphens}` — `english_word` lowercased, spaces and underscores replaced with hyphens, punctuation removed.

| Field | Template | Example |
| - | - | - |
| `audio_word` | `/lessons/media/{book_slug}/{unit_slug}/audio/{word-with-hyphens}.mp3` | `/lessons/media/gs9/unit-1/audio/police-officer.mp3` |
| `audio_sentence` | `/lessons/media/{book_slug}/{unit_slug}/audio/{word-with-hyphens}-sentence.mp3` | `/lessons/media/gs9/unit-1/audio/police-officer-sentence.mp3` |
| `image` | `/lessons/media/{book_slug}/{unit_slug}/images/{word-with-hyphens}.webp` | `/lessons/media/gs9/unit-1/images/police-officer.webp` |
| `alt` | a short English description of what the image should depict | `Image for police officer` |

Images use `.webp`; audio uses `.mp3`. The paths must be consistent across all three media fields for a single word — only the suffix differs.
