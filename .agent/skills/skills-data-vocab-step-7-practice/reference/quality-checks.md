# Quality Checks

This document explains the two checks that run after the 16 files are written — what they enforce, how to interpret the output, and what to do when something fails.

## Coverage check

The coverage script confirms that the Unit's vocabulary actually shows up in the generated exercises. Without this check, it's easy to lean on a familiar set of words and leave a third of the list untouched.

```bash
poetry run python3 .agent/skills/skills-data-vocab-step-7-practice/scripts/vocab_coverage_checker.py <path_to_vocab.json> <path_to_exercises_directory>
```

The script reads every JSON file in the exercises directory, extracts every string value, and counts how many times each `english_word` from `vocab.json` (or one of its standard inflections) appears.

**Target: ≥ 95% coverage.** The script prints the percentage at the top of its report; if it's below 95%, the report also lists the unused words and the high-frequency words (≥ 10 occurrences) that are crowding them out.

### When coverage falls short

The fix has two halves, applied together:

1. **Reduce frequency of overused words.** Find the high-frequency words in the report and rewrite a few of their occurrences to use less-used words instead.
2. **Add the unused words in.** The cleanest place to slot them is exercises 2 (sentence completion) and 3 (conversation completion) — you may expand those exercises in increments of 5 questions if needed. The unused words from the report should be the correct answers (or appear naturally inside the prompts) of the new questions.

After patching, run the coverage script again until it reports ≥ 95%.

### When the script misses an occurrence

The inflection logic in `lemminflect` covers verb conjugations and noun plurals, but it doesn't handle multi-word phrases with insertions. For example, the vocab entry `ride bicycles` won't match a sentence that says `ride **our** bicycles` because of the inserted possessive. If the report flags a word as unused and you can see it in the content (in a form the script can't normalize), you have two choices:

- Rephrase the sentence to use the bare form (`We ride bicycles to school`), or
- Accept the gap if you're already above the 95% target — the script's miss isn't a real coverage hole.

## Final review checklist

After coverage passes, walk through the 16 files one more time. The post-processing scripts handle option position and word-box ordering automatically; everything else is your responsibility.

- **`correct_answer` is accurate.** For multiple-choice questions, the string in `correct_answer` exactly matches one of the strings in `options`. For fill-in-the-blank questions, the answer is the form that fits the sentence (`studies` not `study` for third-person singular).
- **One unambiguous answer per question.** Re-read each MCQ as a student. If two options could both be argued for, revise the question — usually by sharpening the surrounding sentence.
- **Exercise 10 Non-Prefix Antonym Audit.** For `10_multiple_choice_opposite.json`, verify that NO question uses trivial prefix modifications (`in-`, `un-`, `dis-` vs root word) as the correct antonym, ensuring students evaluate vocabulary meaning rather than matching letter prefixes.
- **Exercise 11 4-Pattern Collocation & Non-Interchangeability Audit.** For `dictionary_entry.json`, ensure each entry features 4 syntactically and structurally distinct collocation patterns across its 4 bullet points. Verify that all 4 collocations in each entry are mutually non-interchangeable, each question blank uniquely forces 1 target pattern, and question prompts DO NOT reuse giveaway keywords from the example sentences.
- **Exercise 12 Topic Relevance, Creative Ideas, Multi-Keyword Traps & Deferred Images.** For `signs_and_notices.json`, verify: (1) all 10 items are strictly relevant to the Unit's main topic with fresh, creative scenarios, (2) options distribute topic keywords across multiple choices to avoid single-keyword giveaways, (3) choices use diverse, natural sentence structures rather than copy-pasted templates, (4) options use challenging keyword traps requiring students to read carefully rather than match keywords, (5) question prompts use concise standard stems without embedded context clues, (6) all 4 options per question are balanced to 100% equal character length, (7) options match the prompt's pronoun perspective (use `"We"` when prompt uses `"us"`), and (8) image generation (`generate_image`) was skipped during initial exercise creation so the user can review questions first.
- **Natural phrasing and correct grammar.** Sentences sound like things a native speaker would actually say. No awkward word order, no missing articles, no agreement mistakes.
- **Grammar inside the target Unit's roadmap ceiling.** Nothing in the exercises uses a grammar structure exceeding the target Grade and Unit specified in [`grammar-roadmap.md`](grammar-roadmap.md). (Re-check this for translations in exercise 16 especially — it's easy to slip a future or perfect tense into an English translation before it's taught.)
- **No duplicate sentences or scenarios across exercises.** Each question describes a distinct moment. If two questions feel like they're testing the same idea from slightly different angles, rewrite one of them.
- **Word-box overlap.** The 10 answer words in `paragraph_fill.json` do not overlap with the 10 answer words in `fill_in_blanks.json`.
- **Sentence-ordering cohesion, dialogue format & sequence variety.** In `sentence_ordering.json`, verify: (1) no formulaic transition adverbs (*`Firstly`*, *`Secondly`*, *`Finally`*, *`First of all`*, *`In conclusion`*, *`As a result`*, *`Next`*, *`Afterwards`*) are used as mechanical ordering shortcuts, forcing students to rely on authentic reading comprehension and pronoun cohesion, (2) at least 2 of the 5 questions are in dialogue format, (3) the 5 correct sequences start with at least 3 different letters (a/b/c/d), (4) no two correct sequences are identical, and (5) no correct sequence is `a-b-c-d` (sentences in prompt must always be scrambled).
