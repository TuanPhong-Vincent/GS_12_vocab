# JSON Schemas for the 16 Vocabulary Exercises

Each exercise lives in its own JSON file inside `vocab/exercises/` of the target Unit directory. The filename is fixed — the frontend looks them up by name.

| #   | Filename                            | Type                                | Question count          |
| --- | ----------------------------------- | ----------------------------------- | ----------------------- |
| 1   | `multiple_choice_direct.json`       | `multiple_choice`                   | 10                      |
| 2   | `multiple_choice_sentence.json`     | `multiple_choice`                   | 10                      |
| 3   | `multiple_choice_conversation.json` | `multiple_choice`                   | 10                      |
| 4   | `pic_to_word.json`                  | `pic_to_word`                       | 20                      |
| 5   | `write_english_words.json`          | `write_english_words`               | 10 questions × 2 parts  |
| 6   | `fill_in_blanks.json`               | `fill_in_blanks`                    | 10                      |
| 7   | `paragraph_fill.json`               | `paragraph_fill`                    | 10 blanks               |
| 8   | `sentence_ordering.json`            | `sentence_ordering_multiple_choice` | 5                       |
| 9   | `multiple_choice_closest.json`      | `multiple_choice`                   | 5                       |
| 10  | `multiple_choice_opposite.json`     | `multiple_choice`                   | 5                       |
| 11  | `dictionary_entry.json`             | `dictionary_entry`                  | 5 entries × 2 questions |
| 12  | `signs_and_notices.json`            | `signs_and_notices`                 | 10                      |
| 13  | `word_families_table.json`          | `word_families_table`               | up to 10 rows           |
| 14  | `word_families_mcq.json`            | `word_families_mcq`                 | 10                      |
| 15  | `word_formation.json`               | `word_formation`                    | 5                       |
| 16  | `translate_sentences.json`          | `translate_sentences`               | 10                      |

Each file is a single JSON object (not wrapped in an `exercises` array). The top-level `id` is reassigned automatically by [`scripts/reorder_vocab_ids.py`](../scripts/reorder_vocab_ids.py), so the value you write initially doesn't matter — but every question, part, entry, and blank inside the file needs its own sequential `"1"`, `"2"`, `"3"` … starting from `"1"` for each file.

---

## 1. `multiple_choice_direct.json`

```json
{
  "id": "1",
  "type": "multiple_choice",
  "title": "Multiple Choice - Direct Questions",
  "description": "Choose the best answer for each question.",
  "questions": [
    {
      "id": "1",
      "text": "Which of the following helps save trees?",
      "options": [
        "cutting down forests",
        "reusing paper",
        "wasting water",
        "making noise"
      ],
      "correct_answer": "reusing paper"
    }
  ]
}
```

## 2. `multiple_choice_sentence.json`

```json
{
  "id": "2",
  "type": "multiple_choice",
  "title": "Multiple Choice - Sentence Completion",
  "description": "Choose the correct word to complete the sentence.",
  "questions": [
    {
      "id": "1",
      "text": "We should follow the 3Rs to protect our __________.",
      "options": ["environment", "classroom", "school", "home"],
      "correct_answer": "environment"
    }
  ]
}
```

## 3. `multiple_choice_conversation.json`

```json
{
  "id": "3",
  "type": "multiple_choice",
  "title": "Multiple Choice - Conversation Completion",
  "description": "Choose the correct response to complete the conversation.",
  "questions": [
    {
      "id": "1",
      "text": "Teacher: 'How can we go green?'\nStudent: '______________________________'",
      "options": [
        "By wasting water.",
        "By making more noise.",
        "By planting trees and recycling.",
        "By using more plastic bags."
      ],
      "correct_answer": "By planting trees and recycling."
    }
  ]
}
```

## 4. `pic_to_word.json`

`image` is the absolute path that appears in `vocab.json` for that word — copy it verbatim.

```json
{
  "id": "4",
  "type": "pic_to_word",
  "title": "Write the English Words for the Pictures",
  "description": "Look at each picture and write the correct English word in the blank.",
  "questions": [
    {
      "id": "1",
      "image": "/lessons/media/<book>/<unit>/images/plastic.webp",
      "correct_answer": "plastic"
    }
  ]
}
```

## 5. `write_english_words.json`

10 questions, each with 2 parts → 20 word prompts total.

```json
{
  "id": "5",
  "type": "write_english_words",
  "title": "Write English words",
  "description": "Write the English word for each Vietnamese meaning below.",
  "questions": [
    {
      "id": "1",
      "parts": [
        { "vietnamese": "tái chế", "correct_answer": "recycle" },
        { "vietnamese": "giảm thiểu", "correct_answer": "reduce" }
      ]
    }
  ]
}
```

## 6. `fill_in_blanks.json`

The `word_box` is shuffled later by [`scripts/shuffle_word_box.py`](../scripts/shuffle_word_box.py).

```json
{
  "id": "6",
  "type": "fill_in_blanks",
  "title": "Fill in the Blanks",
  "description": "Complete each sentence with the correct word from the box.",
  "word_box": ["environment", "interview", "tip"],
  "questions": [
    {
      "id": "1",
      "text": "We must protect our __________ for future generations.",
      "correct_answer": "environment"
    }
  ]
}
```

## 7. `paragraph_fill.json`

A single short paragraph rendered from `paragraph_parts`. String entries become plain text; `{ "type": "blank" }` entries become input fields. Every blank carries its own sequential `id`.

```json
{
  "id": "7",
  "type": "paragraph_fill",
  "title": "Fill in the Blanks in the Paragraph",
  "description": "Complete the paragraph below using words from the box.",
  "word_box": ["reduce", "reuse", "recycle"],
  "paragraph_parts": [
    "To protect our ",
    { "id": "1", "type": "blank", "correct_answer": "environment" },
    ", we should follow the 3Rs principle. First, we should ",
    { "id": "2", "type": "blank", "correct_answer": "reduce" },
    " the amount of waste we produce."
  ]
}
```

## 8. `sentence_ordering.json`

Four sentences labelled a-d that form a logical paragraph or short conversation when ordered correctly.

```json
{
  "id": "8",
  "type": "sentence_ordering_multiple_choice",
  "title": "Put the sentences in the correct order",
  "description": "Read the sentences and choose the correct order to form a logical paragraph or conversation.",
  "questions": [
    {
      "id": "1",
      "sentences": [
        "a. In addition, these environments are home to various species of flora and fauna.",
        "b. Secondly, Earth has many natural environments, such as oceans, forests, and grasslands.",
        "c. Finally, protecting these habitats is essential for maintaining the balance of our ecosystems.",
        "d. Firstly, it is the only planet known to support life."
      ],
      "options": ["d-a-c-b", "b-c-d-a", "d-b-a-c", "d-a-b-c"],
      "correct_answer": "d-b-a-c"
    }
  ]
}
```

## 9. `multiple_choice_closest.json`

Target word wrapped in square brackets `[word]` inside `text` — the frontend underlines it.

```json
{
  "id": "9",
  "type": "multiple_choice",
  "title": "Multiple Choice - Closest in Meaning",
  "description": "Choose the word or phrase CLOSEST in meaning to the underlined part.",
  "questions": [
    {
      "id": "1",
      "text": "The new road is very [wide], which helps to reduce congestion and improve the flow of vehicles.",
      "options": ["narrow", "broad", "large", "vast"],
      "correct_answer": "broad"
    }
  ]
}
```

## 10. `multiple_choice_opposite.json`

Same square-bracket convention as exercise 9.

```json
{
  "id": "10",
  "type": "multiple_choice",
  "title": "Multiple Choice - Opposite in Meaning",
  "description": "Choose the word or phrase OPPOSITE in meaning to the underlined part.",
  "questions": [
    {
      "id": "1",
      "text": "Living in the city has a number of [drawbacks].",
      "options": ["negatives", "advantages", "disadvantages", "problems"],
      "correct_answer": "advantages"
    }
  ]
}
```

## 11. `dictionary_entry.json`

5 entries, each with a fake-dictionary look (definition + 4 example sentences with the target phrase in square brackets for bolding + 2 fill-in questions).

**Pedagogical Requirements:**

1. **Target Words**: Prefer words that form interesting collocations.
2. **Collocations as Answers**: The blanks must test full collocations or phrases (e.g., `provide information`, `make a choice`, `take a course`), not just the single headword. The `correct_answer` MUST match exactly the bracketed text in the `bullet_points`. The `bullet_points` must be full, natural sentences containing the bracketed phrase, not just the isolated phrases themselves.
3. **No Context Reuse, Zero Keyword Clues & Unambiguous Collocations**: The `questions` must provide COMPLETELY NEW sentences and contexts. Do NOT reuse the sentences from the `bullet_points` or include giveaway keywords/nouns from them that allow students to guess answers by simple word-matching. Furthermore, the 4 collocations in `bullet_points` must be mutually non-interchangeable, and you must carefully design the question context so that no other collocations from the entry could logically fit into the same blank. The sentence must point unambiguously to ONLY ONE specific collocation. This applies to `bullet_points` as well — do not use contexts where two different phrases could be interchangeable (e.g., "We will [go on a picnic]" vs "We will [have a picnic]").
4. **Literal vs Idiomatic Alignment**: Ensure the example sentences and test questions use the phrase in a way that matches the definition provided for the headword. Do not use idiomatic collocations if they contradict the provided definition (e.g., if the definition of 'cake' is a sweet food, do not use 'a piece of cake' to mean 'very easy').
5. **Grade-Level Appropriateness & Simple Sentence Structures**: All vocabulary and grammar (in both `bullet_points` and `questions`) must strictly stay at or below the target Grade and Unit's level in `grammar-roadmap.md`. For lower grades (like Grade 6), use simple active sentences (Present Simple, Past Simple, Imperatives, basic modal verbs). Avoid unstudied structures such as passive voice, present perfect, complex relative clauses (*where*, *who*, *which*), or heavy participle clauses.
6. **Full Part of Speech Name**: `part_of_speech` MUST be written out in full (e.g., `"noun"`, `"verb"`, `"adjective"`, `"adverb"`). Never use short abbreviations like `"n"`, `"v"`, `"adj"`, `"adv"`.
7. **Inflected / Conjugated Word Forms**: The `correct_answer` in a question sentence should be inflected / conjugated to fit the sentence tense/grammar (e.g. `won a competition` in past tense for `win a competition`), encouraging students to apply both collocation knowledge and proper word forms in context.
8. **Syntactically & Structurally Distinct Collocation Patterns & Strict Length Limit (2–4 words)**: Every bracketed collocation `[...]` MUST be concise, containing STRICTLY 2, 3, OR 4 WORDS (never 5+ words). The target headword of the entry MUST NEVER change its word form in any bullet point or question (e.g., `connect` stays `connect`, `convenient` stays `convenient`). The 4 bullet points must contain 2 pairs of syntactically and structurally distinct collocation patterns of the entire phrase (inspired by real textbook dictionary entries, e.g., for noun `habit`: Noun modifier `eating habits` [2 words] vs Verb+Object `have undesirable habits` [3 words] vs Verb+Prep `develop the habit of` [4 words] vs Phrasal `break the habit` [3 words]; for verb `explore`: `explore unfamiliar areas` [3 words] vs `explore the possibility of` [4 words] vs `explore new ways to` [4 words]). Never use 4 identical sentence templates in an entry. Question 1 tests Group 1's phrase structure (placed in a structural/contextual position requiring that phrase type), and Question 2 tests Group 2's phrase structure (placed in a structural/contextual position requiring that phrase type).

Question `id`s are **globally unique across all entries**: entry 1 → questions 1, 2; entry 2 → questions 3, 4; …

```json
{
  "id": "11",
  "type": "dictionary_entry",
  "title": "Dictionary Entries",
  "description": "Look at the dictionary entries below. Use the information provided to complete the sentences.",
  "entries": [
    {
      "id": "1",
      "word": "provide",
      "part_of_speech": "verb",
      "pronunciation": "/prəˈvaɪd/",
      "definition": "to give something to somebody or make it available for them to use",
      "bullet_points": [
        "Please [provide] the following [information].",
        "The exhibition [provides] an opportunity for local artists to show their work.",
        "We are here to [provide] a service for the public."
      ],
      "questions": [
        {
          "id": "1",
          "text": "The exhibition __________ an opportunity for local artists to show their work.",
          "correct_answer": "provides"
        },
        {
          "id": "2",
          "text": "Please __________ the following information.",
          "correct_answer": "provide"
        }
      ]
    }
  ]
}
```

## 12. `signs_and_notices.json`

10 sign/notice items. All 10 use `sign_type: "image"`. The image path is relative (e.g. `images/sign_1.png`) and the image itself is generated separately and saved to `vocab/exercises/images/`. The `sign_text` is a written description of the sign content used for accessibility and as the prompt for image generation.

**Pedagogical Requirements:**
1. **Unit Topic Relevance & Creative/Novel Scenarios**: All 10 items MUST be strictly themed around the target Unit's core topic (e.g. Unit 10 Energy Sources → renewable energy, solar power, smart saving rules; Unit 11 Future Transport → hyperloops, flying buses, driverless pods). Scenarios must be fresh, creative, and engaging (`lạ và hay`), avoiding cliché textbook defaults.
2. **Anti-Keyword Traps & Deep Reading**: Options MUST NOT be naive or easily guessed by keyword matching. Use exact words from the sign/notice in wrong distractors with altered logic or conditions, forcing students to read both the sign and options thoroughly (`học sinh phải đọc kỹ để chọn đáp án`).
3. **No Image Generation During Exercise Creation**: Do NOT call `generate_image` or generate image files when writing `12_signs_and_notices.json`. Write complete `sign_text` descriptions in the JSON file; image generation is deferred until the user reviews the question content and explicitly requests images.
4. **Diverse Option Structures & Symbol-Only Distribution**: For symbol-only signs (2 Prohibition + 1 Mandatory blue action sign + 2 Warning), use 2 questions with identical starting phrases for direct vocabulary testing, and 3 questions with paraphrased options. Use 8 distinct sign categories across the 10 questions (2 Prohibition, 1 Mandatory blue action sign, 2 Warning, 1 Status sign, 1 Personal message, 1 Announcement email, 1 Advertisement notice, 1 Event poster).
5. **Exact Option Length Balancing**: Trim or pad options so all 4 choices per question are 100% equal in character length.
6. **Standard Concise Question Stems**: The `question` field must be concise and general (e.g. `"What does the sign say?"`, `"What does the notice tell us?"`, `"What does the note say?"`). Do NOT embed detailed situational clues in the question prompt.
7. **Pronoun Agreement & Complete Sentence Options**: Options MUST be complete, unambiguous sentences matching the perspective of the prompt (use `"We"` when the question prompt uses `"us"`). Never use incomplete prepositional fragments.

```json
{
  "id": "12",
  "type": "signs_and_notices",
  "title": "Signs and Notices",
  "description": "Read the sign or notice and choose the correct meaning.",
  "questions": [
    {
      "id": "1",
      "sign_type": "image",
      "sign_image": "images/sign_1.png",
      "sign_text": "A circular prohibition sign showing a crossed-out plastic bag.",
      "question": "What does the sign mean?",
      "options": [
        "Take your bag here.",
        "Use only one plastic bag for each receipt.",
        "No plastic bag is allowed here.",
        "Use banana leaves instead of plastic ones."
      ],
      "correct_answer": "No plastic bag is allowed here."
    }
  ]
}
```

## 13. `word_families_table.json`

Up to 10 rows. Each row picks one base word (the form as it appears in `vocab.json`) and lists every existing form for verb, noun, adjective, adverb. Use an empty array `[]` (NEVER `null`) when a form doesn't exist. `base_word_type` tells the frontend which column to show as the prompt.

```json
{
  "id": "13",
  "type": "word_families_table",
  "title": "Word Families",
  "description": "Complete the table below with different forms of each word. Some forms may not exist.",
  "questions": [
    {
      "id": "1",
      "base_word": "create",
      "base_word_type": "verb",
      "verb": ["create"],
      "noun": ["creation", "creativity"],
      "adjective": ["creative"],
      "adverb": ["creatively"]
    },
    {
      "id": "2",
      "base_word": "education",
      "base_word_type": "noun",
      "verb": ["educate"],
      "noun": ["education"],
      "adjective": ["educational"],
      "adverb": ["educationally"]
    }
  ]
}
```

## 14. `word_families_mcq.json`

```json
{
  "id": "14",
  "type": "word_families_mcq",
  "title": "Multiple Choice – Word Families",
  "description": "Choose the correct word to complete each sentence.",
  "questions": [
    {
      "id": "1",
      "text": "The teacher gave a clear __________ of the 3Rs.",
      "options": ["explain", "explained", "explanation", "explaining"],
      "correct_answer": "explanation"
    }
  ]
}
```

## 15. `word_formation.json`

The base word is **not** appended to the sentence text — the frontend reads `base_word` and renders it separately.

```json
{
  "id": "15",
  "type": "word_formation",
  "title": "Supply the correct form of the word given in each sentence.",
  "description": "Read the sentence and provide the correct form of the word in brackets.",
  "questions": [
    {
      "id": "1",
      "text": "The soup is __________. You must add some salt.",
      "correct_answer": "tasteless",
      "base_word": "TASTE"
    }
  ]
}
```

## 16. `translate_sentences.json`

```json
{
  "id": "16",
  "type": "translate_sentences",
  "title": "Translation",
  "description": "Translate the following sentences into English, using the vocabulary you have learned.",
  "questions": [
    {
      "id": "1",
      "vietnamese": "Chúng ta nên tái chế chai nhựa và thủy tinh.",
      "correct_answer": "We should recycle plastic and glass bottles."
    }
  ]
}
```
