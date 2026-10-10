---
name: data-vocab-step-1-ocr-pdf-to-raw-content
description: Use this skill when the user wants to extract raw content for any Unit in Global Success 12 (GS12 Units 1–10) from the source textbook PDF (GS12.pdf). It slices scanned pages for multimodal vision transcription, extracts the exact textbook texts, and compiles a comprehensive, unified `raw-content.md` containing all sections (Getting Started, Language, Reading, Speaking, Listening, Writing, Communication and Culture/CLIL, Looking Back, Project).
---

# GS12 PDF to Raw-Content Markdown Skill

## Role & Purpose

You are an expert English curriculum specialist and senior educator. Your mission is to extract and compile the complete, authentic unit content from the official **Global Success 12** Student's Book (`GS12.pdf`) into a structured `raw-content.md` file located at `lessons/unit-<N>/vocab/raw-content.md` (or `lessons/unit-<N>/raw-content.md`).

The markdown document must faithfully capture the complete unit content — preserving exact dialogues, reading texts, grammar explanations, vocabulary lists, pronunciation targets, and exercise questions without omission, fabrication, or artificial summarization.

---

## Source PDF File

- **File**: `GS12.pdf` (Student's Book, located at workspace root `d:\GS12\GS12.pdf`)
- **Total Pages**: 155 scanned high-resolution pages.
- **Extraction Mechanism**:
  1. Use script `scripts/pdf2images.py --unit <N> --out temp_pages` to render pages to high-resolution PNG images.
  2. The agent calls `view_file` on each PNG image to visually read and transcribe the content with multimodal vision.
  3. Compile all transcribed sections into the standard `raw-content.md`.
  4. Clean up `temp_pages/` after transcription is complete.

---

## Master Page Mapping for Global Success 12 (GS12.pdf)

All page numbers are 1-indexed (matching PDF viewer page numbers):

| Unit | Title | Target Grammar | Pronunciation | SB Pages (`GS12.pdf`) |
|:---:|:---|:---|:---|:---:|
| **1** | **Life Stories We Admire** | Past simple vs. Past continuous | Diphthongs /eɪ/ and /əʊ/ | **8 – 19** |
| **2** | **A Multicultural World** | Articles (review and extension) | Diphthongs /ɔɪ/, /aɪ/, /aʊ/ | **20 – 31** |
| **3** | **Green Living** | Verbs with prepositions; Relative clauses referring to a whole sentence | Diphthongs /ɪə/, /eə/, /ʊə/ | **32 – 43** |
| *Review 1* | *Units 1 – 3 Review* | Review Units 1 – 3 | Revision | *44 – 47* |
| **4** | **Urbanisation** | Present perfect (review and extension); Double comparatives to show change | Unstressed words in connected speech | **48 – 59** |
| **5** | **The World of Work** | Simple, compound, and complex sentences (review and extension) | Stressing auxiliary and modal verbs | **60 – 71** |
| *Review 2* | *Units 4 – 5 Review* | Review Units 4 – 5 | Revision | *72 – 75* |
| **6** | **Artificial Intelligence** | Active and passive causatives | Homophones | **76 – 87** |
| **7** | **The World of Mass Media** | Adverbial clauses of manner and result | Linking /r/ between two vowels | **88 – 99** |
| **8** | **Wildlife Conservation** | Adverbial clauses of condition and comparison | Assimilation | **100 – 111** |
| *Review 3* | *Units 6 – 8 Review* | Review Units 6 – 8 | Revision | *112 – 115* |
| **9** | **Career Paths** | Three-word phrasal verbs | Sentence stress and rhythm | **116 – 127** |
| **10** | **Lifelong Learning** | Reported speech: reporting orders, requests, offers, and advice | Intonation in questions | **128 – 139** |
| *Review 4* | *Units 9 – 10 Review* | Review Units 9 – 10 | Revision | *138 – 141* |
| *Glossary* | *Alphabetical Wordlist* | Full GS12 vocabulary list | Oxford IPA & Meanings | *142 – 155* |

---

## Standard Structure for `raw-content.md`

Every `raw-content.md` must be organized under the following standard markdown headers:

```markdown
# Unit <N>: <UNIT TITLE>

## This unit includes:
### LANGUAGE
- Pronunciation: ...
- Vocabulary: ...
- Grammar: ...
### SKILLS
- Reading: ...
- Speaking: ...
- Listening: ...
- Writing: ...
### COMMUNICATION AND CULTURE / CLIL
- Everyday English: ...
- Culture / CLIL: ...
### PROJECT
- ...

---

## I. GETTING STARTED
### <Lesson Title>
#### 1. Listen and read. [Track X]
<Full verbatim dialogue>
#### 2. Read the conversation again and ...
#### 3. Find words / phrases in the conversation that mean ...
#### 4. Complete the sentences ...

---

## II. LANGUAGE
### PRONUNCIATION
...
### VOCABULARY
...
### GRAMMAR
...

---

## III. READING
### <Reading Text Title>
<Full reading passage verbatim>
<Questions & exercises 1 to 5>

---

## IV. SPEAKING
...

---

## V. LISTENING
<Audio scripts if available or comprehension tasks>

---

## VI. WRITING
<Writing task guidelines, outline, model sample>

---

## VII. COMMUNICATION AND CULTURE / CLIL
### Everyday English
### Culture / CLIL
<Cultural reading text verbatim>

---

## VIII. LOOKING BACK
### Pronunciation
### Vocabulary
### Grammar

---

## IX. PROJECT
<Project description and presentation prompt>
```

---

## Execution Workflow

1. Determine target unit `<N>` (e.g. Unit 4).
2. Check page range from Master Mapping (e.g. pages 48 to 59).
3. Run extraction script:
   ```powershell
   python .agent/skills/skills-data-vocab-step-1-ocr-raw-content/scripts/pdf2images.py --unit <N> --out temp_pages/u<N>
   ```
4. Read each page image using `view_file` to capture exact texts and questions.
5. Save the transcribed content to `lessons/unit-<N>/vocab/raw-content.md` (or `lessons/unit-<N>/raw-content.md`).
6. Clean up `temp_pages/u<N>/`.
