# JSON Schemas for Grammar Exercises & `grammar_raw.json`

This document defines the strict JSON schemas for the grammar practice exercise datasets.
The exercises are saved as modular JSON files in `<lesson_folder>/grammar/exercises/` (or `<lesson_folder>/grammar/`) and compiled into `<lesson_folder>/grammar_raw.json`.

---

## Overview of Grammar Exercise Datasets

| File | Exercise Name | Type | Question Count | Core Grammar Focus |
|---|---|---|---|---|
| `01_mcq.json` | Multiple Choice Questions | `multiple_choice` | 20 questions | Target grammar point with 4 plausible distractors |
| `02_verbform.json` | Verb Form & Conjugation | `verb_form` | 20 questions | Verbs in brackets requiring correct conjugation/form |
| `03_matching.json` | Match Sentence Halves | `matching_halves` | 10 pairs | Clause / structure halves forming coherent sentences |
| `04_rewrite.json` | Sentence Transformation | `sentence_transformation` | 10 questions | Rewriting sentences with cues/prompts (paraphrasing) |
| `05_guided_cloze.json` | Guided Cloze Passages | `guided_cloze` | 2 passages (20 Qs each = 40 Qs) | In-context reading cloze testing target grammar & connectors |
| `06_error_identification.json` | Error Identification | `error_identification` | 10 questions | 4 underlined sections (A, B, C, D) with error detection & fix |
| `07_sentence_combination.json` | Sentence Combination | `sentence_combination` | 10 questions | Combining two sentences into one using target conjunctions |
| `08_sentence_building.json` | Sentence Building | `sentence_building` | 10 questions | Slashed cue phrases reconstructed into complete sentences |
| `grammar_raw.json` | Consolidated Master Dataset | `composite` | All exercises | Master format loaded by HTML/PDF generators |

---

## 1. `01_mcq.json` (20 questions)

```json
{
  "id": "1",
  "type": "multiple_choice",
  "title": "Exercise 1: Multiple Choice Questions",
  "instruction": "Choose the best answer (A, B, C, or D) that correctly applies the target grammar point.",
  "target_grammar": "Past simple vs. Past continuous",
  "questions": [
    {
      "id": "1",
      "text": "While the dedicated botanist ______ rare alpine species in the valley, she discovered an unclassified orchid.",
      "options": [
        "was documenting",
        "documented",
        "documents",
        "has documented"
      ],
      "correct_answer": "was documenting",
      "explanation": "Hành động kéo dài đang diễn ra trong quá khứ dùng thì Quá khứ tiếp diễn ('was documenting') sau liên từ 'While'."
    }
  ]
}
```

*Requirements*:
- Exactly 20 questions (`id`: "1" to "20").
- `options`: Array of 4 unique, plausible choices.
- `correct_answer`: Exactly matching one option string.
- Options balanced evenly across positions A (0), B (1), C (2), D (3) (~5 questions each).
- Concise bilingual or Vietnamese `explanation` for each question.

---

## 2. `02_verbform.json` (20 questions)

```json
{
  "id": "2",
  "type": "verb_form",
  "title": "Exercise 2: Verb Form & Conjugation",
  "instruction": "Complete each sentence with the correct form or tense of the verb in brackets.",
  "target_grammar": "Past simple vs. Past continuous",
  "questions": [
    {
      "id": "1",
      "text": "The volunteers (renovate) ______ the community center when a sudden thunderstorm interrupted their work.",
      "verb": "renovate",
      "correct_answer": "were renovating",
      "explanation": "Hành động đang diễn ra trong quá khứ ('were renovating') bị hành động ngắn hơn cắt ngang ('interrupted')."
    }
  ]
}
```

*Requirements*:
- Exactly 20 questions (`id`: "1" to "20").
- `text`: Sentence containing `(base_verb) ______`.
- `verb`: Base form in parentheses.
- `correct_answer`: Correctly inflected verb or verb phrase.
- `explanation`: Clear grammatical rule justification.

---

## 3. `03_matching.json` (10 questions / pairs)

```json
{
  "id": "3",
  "type": "matching_halves",
  "title": "Exercise 3: Match the Sentence Halves",
  "instruction": "Match the sentence beginnings (1–10) with the appropriate endings (A–J) to form meaningful and grammatically accurate sentences.",
  "target_grammar": "Past simple vs. Past continuous",
  "questions": [
    {
      "id": "1",
      "half_a": "While Dr. Alvarez was analyzing the water samples,"
    },
    {
      "id": "2",
      "half_a": "The archaeological team made a breakthrough discovery"
    }
  ],
  "options": [
    {
      "label": "A",
      "half_b": "she detected high concentrations of microplastics."
    },
    {
      "label": "B",
      "half_b": "while they were excavating the ancient temple foundation."
    }
  ],
  "correct_matches": {
    "1": "A",
    "2": "B"
  }
}
```

*Requirements*:
- Exactly 10 questions (`id`: "1" to "10").
- Exactly 10 options labeled `"A"` through `"J"`.
- `correct_matches`: Dictionary mapping each question ID to its correct option label.
- Demonstrates clear grammatical clause relationships (conjunctions, clauses of reason/result/time/condition).

---

## 4. `04_rewrite.json` (10 questions)

```json
{
  "id": "4",
  "type": "sentence_transformation",
  "title": "Exercise 4: Sentence Transformation",
  "instruction": "Rewrite each sentence using the cue or bold word provided so that it has the closest meaning to the original sentence.",
  "target_grammar": "Past simple vs. Past continuous",
  "questions": [
    {
      "id": "1",
      "original_sentence": "During their expedition across the rainforest, they encountered an endangered gibbon species.",
      "cue": "While",
      "correct_answer": "While they were traveling across the rainforest, they encountered an endangered gibbon species.",
      "acceptable_answers": [
        "While they were traveling across the rainforest, they encountered an endangered gibbon species.",
        "While they were on an expedition across the rainforest, they encountered an endangered gibbon species."
      ],
      "explanation": "Chuyển cụm giới từ 'During their expedition' thành mệnh đề trạng ngữ chỉ thời gian với 'While + past continuous'."
    }
  ]
}
```

*Requirements*:
- Exactly 10 questions (`id`: "1" to "10").
- `original_sentence`: Clear, authentic sentence.
- `cue`: Starting word or prompt (e.g., "While", "When", "Because of", "It was...", "Having + V3").
- `correct_answer`: Primary gold-standard answer.
- `acceptable_answers`: Array of valid syntactic variants.
- `explanation`: Pedagogical tip explaining the transformation rule.

---

## 5. `05_guided_cloze.json` (2 passages, 20 questions each)

```json
{
  "id": "5",
  "type": "guided_cloze",
  "title": "Exercise 5: Guided Cloze Passages",
  "instruction": "Read the passages below and choose the best answer (A, B, C, or D) for each numbered blank.",
  "target_grammar": "Target Grammar in Context",
  "passages": [
    {
      "passage_id": "1",
      "title": "A Legacy of Courage and Vision",
      "content": "When Dr. Maya first arrived in the rural province, local communities (1) ______ severe shortages of medical supplies. While she (2) ______ a makeshift mobile clinic...",
      "questions": [
        {
          "id": "1",
          "blank_number": 1,
          "options": ["were experiencing", "experienced", "experience", "had experienced"],
          "correct_answer": "were experiencing",
          "explanation": "Hành động diễn tả bối cảnh đang diễn ra tại thời điểm quá khứ."
        }
      ]
    },
    {
      "passage_id": "2",
      "title": "The Evolution of Urban Living",
      "content": "Passage text with blanks (21) to (40)...",
      "questions": [
        {
          "id": "21",
          "blank_number": 21,
          "options": ["...", "...", "...", "..."],
          "correct_answer": "...",
          "explanation": "..."
        }
      ]
    }
  ]
}
```

*Requirements*:
- Exactly 2 passages (`passage_id`: "1" and "2").
- Passage 1 has 20 blanks numbered 1 to 20 (`questions` count = 20).
- Passage 2 has 20 blanks numbered 21 to 40 (`questions` count = 20).
- Total questions across both passages: 40 questions.
- Every question has 4 options (A, B, C, D) with balanced keys (~5 of each letter per passage).
- Passages deeply integrate the thematic vocabulary and discourse flow of the unit.

---

## 6. `06_error_identification.json` (10 questions)

```json
{
  "id": "6",
  "type": "error_identification",
  "title": "Exercise 6: Error Identification & Correction",
  "instruction": "Identify the underlined part (A, B, C, or D) that contains a grammatical mistake, then provide the correct form.",
  "target_grammar": "Past simple vs. Past continuous",
  "questions": [
    {
      "id": "1",
      "text": "While the environmentalists [A: were inspecting] the polluted river, they [B: notice] that hazardous chemicals [C: were leaking] into the drinking water [D: supply].",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "B",
      "error_segment": "notice",
      "correction": "noticed",
      "explanation": "'notice' là hành động ngắn xen vào quá trình kiểm tra ('were inspecting'), phải chia thì Quá khứ đơn 'noticed'."
    }
  ]
}
```

*Requirements*:
- Exactly 10 questions (`id`: "1" to "10").
- `text`: Displays 4 clearly bracketed options `[A: ...]`, `[B: ...]`, `[C: ...]`, `[D: ...]`.
- `options`: Always `["A", "B", "C", "D"]`.
- `correct_answer`: The letter containing the mistake.
- `error_segment`: The erroneous phrase.
- `correction`: The correct grammatical replacement.
- `explanation`: Detailed grammar explanation.

---

## 7. `07_sentence_combination.json` (10 questions)

```json
{
  "id": "7",
  "type": "sentence_combination",
  "title": "Exercise 7: Sentence Combination",
  "instruction": "Combine each pair of sentences into a single, cohesive sentence using the target grammatical structure indicated.",
  "target_grammar": "Past simple vs. Past continuous",
  "questions": [
    {
      "id": "1",
      "sentence_1": "The software engineer was debugging the neural network.",
      "sentence_2": "Suddenly, a critical security breach was detected.",
      "cue": "Use 'When'",
      "correct_answer": "The software engineer was debugging the neural network when a critical security breach was detected.",
      "acceptable_answers": [
        "The software engineer was debugging the neural network when a critical security breach was detected.",
        "When a critical security breach was detected, the software engineer was debugging the neural network."
      ],
      "explanation": "Dùng 'when' kết nối hành động xen vào thì Quá khứ đơn với hành động đang tiếp diễn."
    }
  ]
}
```

*Requirements*:
- Exactly 10 questions (`id`: "1" to "10").
- `sentence_1` and `sentence_2`: Two logically connected statements.
- `cue`: Specified conjunction or grammatical form.
- `correct_answer` and `acceptable_answers`.
- `explanation`: Vietnamese grammatical guide.

---

## 8. `08_sentence_building.json` (10 questions)

```json
{
  "id": "8",
  "type": "sentence_building",
  "title": "Exercise 8: Sentence Building from Cues",
  "instruction": "Use the cue words and phrases to form grammatically correct and meaningful sentences using the target grammar.",
  "target_grammar": "Past simple vs. Past continuous",
  "questions": [
    {
      "id": "1",
      "cues": "While / team / conduct / ecological survey / they / encounter / endangered leopard",
      "correct_answer": "While the team was conducting an ecological survey, they encountered an endangered leopard.",
      "acceptable_answers": [
        "While the team was conducting an ecological survey, they encountered an endangered leopard."
      ],
      "explanation": "Thêm liên từ, mạo từ và chia động từ: 'was conducting' (hành động dài) và 'encountered' (hành động ngắn)."
    }
  ]
}
```

*Requirements*:
- Exactly 10 questions (`id`: "1" to "10").
- `cues`: Slash-separated stems.
- `correct_answer`: Complete, natural English sentence.
- `explanation`: Detailed explanation of required morphological and grammatical additions.

---

## 9. Consolidated `grammar_raw.json`

The consolidated master file combines all exercises into a single structured object:

```json
{
  "grade": "GS12",
  "unit": 1,
  "unit_theme": "Life Stories We Admire",
  "grammar_topic": "Past simple vs. Past continuous",
  "total_exercises": 8,
  "total_questions": 120,
  "exercises": {
    "ex1_mcq": { ... },
    "ex2_verbform": { ... },
    "ex3_matching": { ... },
    "ex4_rewrite": { ... },
    "ex5_guided_cloze": { ... },
    "ex6_error_identification": { ... },
    "ex7_sentence_combination": { ... },
    "ex8_sentence_building": { ... }
  }
}
```
