# Exercise Rules

This document covers content rules that apply across all 16 exercises, plus the small set of per-exercise instructions that go beyond what the schema in [`json-schemas.md`](json-schemas.md) shows.

## Cross-cutting rules

These apply to every exercise. They protect either the dataset's integrity or the student's experience — keep them in mind whenever you draft a question.

### Originality

Don't reuse `example_sentence_en` from `vocab.json` or sentences from `raw-content.md` (or `raw-all-content.md` if the Unit uses that filename). Do not use any ideas, contexts, names, or entities from them. Students should encounter the vocabulary inside completely fresh prose and scenarios. Invent new scenarios; do not paraphrase or lift phrases.

### Sentence uniqueness across the file set

No two questions — even across different exercise files — should share the same meaning or scenario. If you find yourself writing "Mai has a heavy school bag" in one exercise and "Lan's school bag is heavy" in another, vary the subject, the verb, or the situation. Each sentence should describe a distinct moment.

### Context diversity and topic alignment (Đa dạng hóa ngữ cảnh & Bám sát chủ đề)

- **Diverse yet focused contexts**: Questions across all exercises must explore a rich variety of engaging, realistic situations. However, all scenarios must remain firmly anchored to the Unit's core theme or closely related thematic areas (e.g. for a "Cities of the World" unit, explore landmarks, travel experiences, weather, transport, street food, holiday postcards, and cultural facts).
- **Maximize vocabulary utilization**: Actively exploit the full breadth of the Unit's vocabulary set across exercises rather than clustering questions around a handful of familiar words.
- **Controlled context expansion**: Minor, natural expansion of related contexts is encouraged to keep questions lively and prevent repetitive phrasing, but all sentences must strictly stay at or below the target grade's English proficiency ceiling (`grammar-roadmap.md`) without introducing obscure or unstudied words.

### Grammar alignment

The grammar in every generated sentence must strictly stay at or below the target Grade and Unit's level as defined in [`grammar-roadmap.md`](grammar-roadmap.md). Check the target grade and unit in the roadmap before writing: if the target is Grade 6 Unit 3 (Present continuous), you may only use Present simple, Adverbs of frequency, Possessive, Prepositions of place, and Present continuous. **Do NOT use grammar structures from higher units or higher grades** (e.g. Past simple, passive voice, complex conditionals, perfect tenses) because students have not learned them yet. When in doubt, simpler is better — students should be able to parse every sentence easily without encountering unstudied grammar.

### One unambiguous answer per question

Every question — multiple-choice, fill-in-the-blank, ordering, dictionary fill — has exactly one defensible correct answer. Distractors are clearly wrong, not "wrong in this context but correct in another". Before finalizing a question, re-read it as a student would and ask: *could a student reasonably argue for a different answer?* If yes, revise the question (usually by tightening the surrounding context or replacing the ambiguous distractor).

### Word variations are encouraged

You can and should inflect vocabulary words to make sentences natural. `vocab.json` lists `make up` — your sentence may use `makes up`, `making up`, `made up` (within the grammar ceiling). The coverage checker in [`scripts/vocab_coverage_checker.py`](../scripts/vocab_coverage_checker.py) uses `lemminflect` to recognize standard inflections, so plurals and conjugations still count toward coverage.

### Question IDs

Every question, part, entry, and blank object gets an `"id"` field. IDs are strings (`"1"`, `"2"`, `"3"` …) and they are sequential within the file, starting from `"1"`. The top-level `id` on the file itself is set by [`scripts/reorder_vocab_ids.py`](../scripts/reorder_vocab_ids.py) during post-processing — you don't need to get it right initially.

For `dictionary_entry.json` (exercise 11), question IDs are **globally unique across all entries**: entry 1 has questions `"1"` and `"2"`, entry 2 has questions `"3"` and `"4"`, etc.

### Word-box overlap rule

The words used as **answers** in `paragraph_fill.json` (exercise 7) must be entirely different from the words used as answers in `fill_in_blanks.json` (exercise 6). Both exercises share the same fill-in-the-blank format with a `word_box`, so reusing the same vocabulary between them would feel repetitive to students. (Other exercise types may reuse words freely — only these two are constrained.)

## Per-exercise notes

The schema in [`json-schemas.md`](json-schemas.md) shows the shape of each file. This section covers the smaller content rules that don't fit in a schema example.

### Exercise 1 — Multiple Choice, Direct Questions (10)

Conceptual questions about the vocabulary — *which place has many books?*, *which subject is about numbers?* Avoid translation questions; those belong in exercise 16.

### Exercise 2 — Multiple Choice, Sentence Completion (10)

A sentence with one blank and four single-word (or short-phrase) options. Keep the surrounding sentence simple enough that only one option fits.

### Exercise 3 — Multiple Choice, Conversation Completion (10)

A two-line conversation where the second speaker's line is missing. Replace it with four full-sentence options. Ensure that at least 5 of these questions represent common communication models (e.g., responding to a compliment, invitation, request, or apology) so students learn standard conversational responses.

Three rules unique to this exercise:

- **Options are complete sentences**, not fragments or single words.
- **Diverse responses and distractors.** Use a variety of communication functions and ensure the distractors are diverse and contextually appropriate. Avoid recycling the same standard phrases (like "You're welcome", "Yes, please", "I'm sorry") across multiple questions as distractors.
- **Option lengths are roughly balanced.** If the correct answer is noticeably longer or richer in detail than the distractors, students will guess from the shape alone without reading. Trim or pad the distractors so all four lines look interchangeable at a glance.

### Exercise 4 — Pic to Word (20)

20 words drawn from `vocab.json`, each paired with its `image` path copied verbatim. Pick visually distinct words — abstract concepts like *reason* or *advice* don't translate to a clear picture; concrete nouns like *playground*, *uniform*, *swimming pool* do.

### Exercise 5 — Write English Words (10 questions × 2 parts)

Vietnamese → English direct translation of single words. Pull pairs from `vocab.json` and split them across 10 questions of 2 parts each (20 word prompts total).

### Exercise 6 — Fill in the Blanks (10)

10 sentences with one blank each. The `word_box` lists all 10 answers in any order — [`scripts/shuffle_word_box.py`](../scripts/shuffle_word_box.py) will randomize the display order during post-processing.

### Exercise 7 — Paragraph Fill (10 blanks)

A single coherent paragraph (one topic, one narrator) containing 10 blanks. See the [word-box overlap rule](#word-box-overlap-rule) above — the 10 answer words must not appear as answers in exercise 6.

### Exercise 8 — Sentence Ordering MCQ (5)

Five questions, each with four sentences labelled a/b/c/d that combine into a logical paragraph or short conversation.

Pedagogical, content, and design rules:

- **No Formulaic Opening Transition Adverbs (Loại bỏ các cụm trạng từ mở đầu công thức)**:
  - DO NOT rely on formulaic opening transition adverbs (e.g. *`First`*, *`Firstly`*, *`First of all`*, *`Secondly`*, *`Next`*, *`Afterwards`*, *`At the start`*, *`As a result`*, *`In conclusion`*, *`Finally`*).
  - Using these adverbs lowers pedagogical value because students can mechanically solve the ordering (e.g. `First` $\rightarrow$ `Next` $\rightarrow$ `Finally`) without reading or understanding the sentence content.
  - Sentence ordering logic MUST rely on authentic cohesion: pronoun references (`this device`, `these compact scanners`, `they`), cause-and-effect relationships, temporal/narrative flow, and natural question-answer dialogue pairs.
- **Mandatory Dialogue-Format Questions (Ít nhất 2 câu dạng hội thoại)**:
  - Out of the 5 questions, **at least 2 questions MUST be in dialogue format** (short 4-turn conversations between two speakers, e.g. Person A asks $\rightarrow$ Person B answers $\rightarrow$ Person A follows up $\rightarrow$ Person B confirms).
  - The remaining questions should be narrative or informative paragraphs (topic sentence $\rightarrow$ detail $\rightarrow$ mechanism/explanation $\rightarrow$ outcome/benefit).
- **Shuffle the starting labels**:
  - Don't always assign the intro sentence to label `a`. Across the 5 questions, the correct sequences must start with at least **3 different letters** (e.g. `a`, `b`, `c`, `d`).
- **No two questions share the same correct sequence**:
  - All 5 correct answers must be distinct sequence strings.
- **Always scramble prompt sentences (Never use `a-b-c-d` as correct sequence)**:
  - Sentences listed under `sentences` MUST be scrambled so the correct answer is NEVER `a-b-c-d` (which would mean the prompt sentences were already in order without scrambling).

### Exercise 9 — Closest in Meaning (5) and Exercise 10 — Opposite in Meaning (5)

Wrap the target word in square brackets `[word]` inside the question text — the frontend underlines it. The four options are candidate synonyms (exercise 9) or antonyms (exercise 10); only one is correct in this exact context.

- **No Trivial Prefix Giveaways in Exercise 10 (Cấm dùng từ trái nghĩa bằng tiền tố lộ đáp án)**:
  - DO NOT use trivial prefix modifications as the correct antonym (e.g. avoiding `convenient` $\rightarrow$ `inconvenient`, `available` $\rightarrow$ `unavailable`, `helpful` $\rightarrow$ `unhelpful`, `independent` $\rightarrow$ `dependent`, `happy` $\rightarrow$ `unhappy`).
  - Using prefix giveaways allows students to select the answer mechanically without reading or understanding the sentence.
  - Instead, use rich, natural, non-prefix antonyms appropriate for the target Grade (e.g., `convenient` $\rightarrow$ `troublesome`, `independent` $\rightarrow$ `controlled`, `available` $\rightarrow$ `sold-out`, `helpful` $\rightarrow$ `useless`).

### Exercise 11 — Dictionary Entry (5 entries × 2 questions)

Pick 5 single-word vocabulary items (no phrases or compound terms) from the Unit that are difficult or academic (e.g., `creativity`, `responsibility`, `maturity`, `valuable`, `benefit`). For each:

- Write a fake-dictionary entry: `word`, `part_of_speech` (**must be written out in full, e.g. `noun`, `verb`, `adjective`, `adverb` — NEVER use single-letter or short abbreviations like `n`, `v`, `adj`, `adv`**), `pronunciation` (use the same phonetic spelling as `vocab.json`), a short `definition`, and **exactly 4 `bullet_points`** showing common collocations or example uses. **STRICT COLLOCATION LENGTH RULE: Every bracketed collocation `[...]` MUST be concise, containing STRICTLY 2, 3, OR 4 WORDS (never 5+ words).** **CRITICAL HEADWORD RULE: The target headword MUST NEVER change its word form in any bullet point or question (e.g. `connect` must stay `connect` — NEVER use `connection`; `convenient` must stay `convenient` — NEVER use `convenience`).** The 4 bullet points must feature **4 syntactically and structurally distinct collocation patterns** of the ENTIRE PHRASE using the exact headword (inspired by authentic dictionary entries, e.g., for noun `habit`: Pattern 1 Noun modifier `eating habits` [2 words], Pattern 2 Verb+Object `have undesirable habits` [3 words], Pattern 3 Verb+Prep `develop the habit of` [4 words], Pattern 4 Phrasal `break the habit` [3 words]; for verb `explore`: Pattern 1 `explore unfamiliar areas` [3 words], Pattern 2 `explore the possibility of` [4 words], Pattern 3 `explore new ways to` [4 words], Pattern 4 `explore with local guides` [4 words]). **NEVER use identical sentence templates across bullet points in the same entry**, as identical templates lead to ambiguous, interchangeable questions. **These bullet points should only show general usage in an example sentence and must not be identical or contextually parallel to the questions.**
- Add **exactly 2 fill-in-the-blank questions**. **Each question tests a specific collocation pattern placed in a syntactic/structural position that uniquely requires that exact phrase type, preventing any confusion with the other 3 collocations.** Crucially, the sentences in these questions must be entirely new contexts and MUST NOT reuse key nouns, verbs, or domain vocabulary from the bullet points. The student must analyze the collocations in the dictionary entry and apply them based on the context of the new sentence. **Inflecting / conjugating verbs in collocations is encouraged when required by sentence tense or grammar context** (e.g., if a bullet point shows `[win a competition]`, a past-tense question sentence should test `[won a competition]` as the `correct_answer`).

#### Strict Anti-Interchangeability & Zero Keyword-Clue Design Strategies

Two major flaws frequently ruin dictionary exercises: (1) creating questions where multiple collocations from the same entry can fit into the same blank (e.g. `Sherlock Holmes is a [famous character / main character / interesting character]`), and (2) making questions trivial by reusing key words from the example sentences (e.g. using `paint and draw` in both the bullet point and the question, allowing students to blindly match words without reading). To guarantee **100% unambiguous single answers** and **true comprehension testing**, you MUST apply the following six design strategies:

1. **Collocation Diversity (4 Mutually Non-Interchangeable Syntactic Patterns)**:
   - Do NOT choose collocations that share identical grammatical templates (e.g. 4 generic adjective + noun modifiers like `famous character`, `main character`, `popular character`, `interesting character` where any adjective fits any person).
   - Instead, select **4 syntactically or semantically distinct collocations**:
     - *4 Distinct Structural Patterns*: e.g., for noun `habit`: Noun modifier (`eating habits`), Verb Object (`have undesirable habits`), Verb + Prep (`develop the habit of [doing sth]`), Phrasal (`break the habit of [doing sth]`).
     - *Distinct Prepositions*: e.g. `connect with [friends]` vs `connect to [Wi-Fi]`.
     - *Distinct Syntactic Functions*: e.g. `account password` (noun compound modifier) vs `create an account` (verb object).
     - *Distinct Target Entities*: e.g. `convenient time` (schedule/time) vs `convenient location` (place/facility).
     - *Distinct Recipient / Action Roles*: e.g. `translate speech` (spoken audio) vs `translate sentences` (written text).

2. **Explicit Context-Forcing & Syntactic Triggers**:
   - Question sentences must restrict the blank to ONLY ONE specific collocation using structural or contextual triggers:
     - *Syntactic Category Triggers*: When an entry contains collocations of different phrase structures (e.g., `explore the possibility of + V-ing` vs `explore new ways to + Verb`), placing the blank before a gerund (`expanding...`) or infinitive (`reduce...`) naturally forces the answer to the exact matching collocation.
     - *Preposition / Domain / Actor Triggers*: For collocations of the same word type, use prepositions before/after the blank (`connect with [friends]` vs `connect to [Wi-Fi]`), domain triggers, or object roles.

3. **Zero Keyword Clues / Anti-Word-Matching (Prevent Easy Guessing)**:
   - The test question sentences MUST NOT contain giveaway keywords, nouns, or specific situational terms used in the bullet point example sentences.
   - *Bad example*: 
     - Bullet point: *"Children can **express creativity** by painting pictures and drawing."*
     - Question (FLAWED): *"In art class, students can __________ by painting pictures."* (Trivial: word-matching on 'painting pictures').
   - *Good example*: 
     - Bullet point: *"Children can **express creativity** by painting pictures and drawing."*
     - Question (CORRECT): *"The architecture competition gives young designers a chance to __________ through innovative building concepts."* (Requires understanding the meaning of 'express creativity' in a fresh context).

4. **Mandatory Dual-Audit (Interchangeability & Keyword Check)**:
   - Before finalizing Exercise 11, test ALL 4 collocations from the dictionary entry in Question A's blank and Question B's blank. Verify that **only 1 collocation fits** and the other 3 are strictly impossible.
   - Scan the question sentence against all 4 bullet point sentences. If any non-target key noun or verb is repeated between a bullet point and a question prompt, **rewrite the question prompt immediately**.

5. **Strict Grade-Level Grammar Ceiling & Elementary Non-Target Vocabulary**:
   - All sentences (both `bullet_points` example sentences and `questions` prompts) MUST strictly stay at or below the target Grade and Unit's level as defined in [`grammar-roadmap.md`](grammar-roadmap.md).
   - For lower grades (e.g., Grade 6), do NOT use passive voice (*was recognized*, *is required*), present perfect (*has hosted*), complex relative clauses (*where*, *who*, *which*), or heavy participle phrases. 
   - Keep sentence structures simple and active (Present Simple, Past Simple, Imperatives, basic modals like *must*, *can*, *should*) with elementary/grade-appropriate non-target vocabulary so that students focus on understanding the collocation without struggling with complex grammar or unstudied words.

6. **Inflected / Conjugated Word Forms in Answers (Chia dạng từ khi cần thiết)**:
   - Question sentences should require students to inflect / conjugate the verb inside the collocation to match the sentence tense (e.g., if a bullet point defines `[win a competition]`, a past simple question sentence should require `[won a competition]` as the `correct_answer`).
   - Using inflected forms is encouraged whenever natural so that students practice both collocation recognition and grammatical word-form conjugation in context.

7. **4 Distinct Phrase Structure Collocation Design Rule**:
   - For every dictionary entry (which has 4 bullet points and 2 questions):
     - **Unchanged Headword**: The target word of the entry MUST NEVER change its form in any bullet point (e.g., `connect` stays `connect`, `convenient` stays `convenient`).
     - **Bullet Points (4 Distinct Syntactic Collocation Patterns)**: The 4 bullet points MUST contain **4 syntactically and structurally distinct collocation patterns** of the entire phrase (e.g., for verb `connect`: Pattern 1 `connect with [people]`, Pattern 2 `connect to [networks]`, Pattern 3 `connect [two objects] together`, Pattern 4 `help connect [users]`).
     - **Questions**: Each question blank is placed in a syntactic/contextual position requiring its specific pattern, pointing uniquely to 1 target phrase without any ambiguity or confusion.
   - This distinct structure ensures that every entry tests both grammatical form recognition and deep reading comprehension.

Question IDs in this file are globally unique across all 5 entries — see [Question IDs](#question-ids).

### Exercise 12 — Signs and Notices (10)

Each item is a sign, notice, message, or email rendered as an image. The image itself is generated separately — your job is to write the `sign_text` description (used as both the alt text and the image-generation prompt) plus four candidate interpretations.

Strictly follow this structure and distribution for the 10 questions:

1. **Prohibition signs (2 questions)** — circular red crossed-out symbol. **MUST HAVE NO TEXT** on the sign itself (only symbols, e.g., a crossed-out bicycle or swimmer).
2. **Mandatory/Instructional signs (1 question)** — circular blue mandatory action sign (e.g. wearing sports shoes or helmet). **MUST HAVE NO TEXT** on the sign itself (only white symbols on a blue circle).
3. **Warning/hazard signs (2 questions)** — yellow/orange triangles or diamonds. **MUST HAVE NO TEXT** on the sign itself (only symbols, e.g., slippery floor icon, fire icon).
4. **Instructional/status signs (1 question)** — rectangles indicating a current state (*Quiet please — exam in progress*).
5. **Personal notes/messages (1 question)** — informal handwritten notes or text messages (*Hi Mai, I can't make it to practice today…*).
6. **Short emails/announcements (1 question)** — addressed to parents, students, staff (*Dear parents, school will close at 12 p.m. on Friday*).
7. **Advertisements/promotional notices (1 question)** — sales, discounts, conditions (*50% off today*).
8. **Event flyers/posters (1 question)** — dates, times, locations for clubs or events.

Pedagogical, content, and design rules:

- **Unit Topic Relevance & Creative/Novel Scenarios (Ý tưởng phải liên quan đến chủ đề của Unit, ý tưởng lạ và hay)**:
  - ALL 10 signs, notices, sticky notes, emails, ads, or flyers MUST be strictly themed around the target Unit's main topic (e.g. Unit 10 Energy Sources → solar charger rules, wind farm visitor safety, smart energy-saving notices, green power exhibitions; Unit 11 Future Transport → hyperloop station boarding rules, driverless pod emergency procedures, flying bus ticket policies).
  - Question contexts and scenarios must be fresh, realistic, novel, and engaging (`lạ và hay`) — avoid standard generic textbook clichés (e.g., standard "No smoking" or "Quiet area") unless given a clever, unit-themed twist.
- **Deep Reading, Diverse Structures & Multi-Keyword Distractors (Đa dạng hóa cấu trúc câu + Trộn lẫn Keyword đánh lừa ở nhiều phương án)**:
  - **No Single-Keyword Giveaways**: NEVER create a question where the main topic/icon keyword (e.g. *Wi-Fi, Bluetooth, magnetic, safety eye gear, toxic chemicals, drone, AI system, project, conference, nanolearning, contest*) appears ONLY in the correct answer. If a student can scan options, spot the keyword in only one choice, and pick it without reading, the question is FLAWED.
  - **Multi-Option Keyword Distribution**: The core icon/topic keyword or closely related domain terms MUST be distributed across multiple choices (in 2 to 4 options) with different meanings, conditions, or actions (e.g., *banned vs free vs increased vs required*; *banned vs on discount vs free to use*; *required vs sold vs washed vs optional*).
- **Function Alignment & Rich Varied Sentence Structures (Đồng bộ chức năng câu nhưng đa dạng hóa cấu trúc ngữ pháp giữa các phương án)**:
  - Distractors MUST align with the general function of the sign or notice (e.g., for prohibition signs, distractors must express prohibitions or restrictions so students cannot eliminate options simply because they are positive or permissive).
  - **CRITICAL**: Use **varied, natural English grammar structures** across the 4 options rather than copy-pasting 1 repetitive sentence template across all choices (e.g., for prohibition signs, mix structures like `Gerund + is not allowed`, `Visitors must not...`, `... is strictly prohibited`, `Do not + Verb`). This tests real reading comprehension, makes the exercise feel like authentic Cambridge/PET exams, and prevents robotic, formulaic options.
  - Apply this structure variety across all types:
    - **Prohibition signs** (Q1–Q2): Combine `Gerund + is not allowed`, `must not...`, `... is strictly prohibited`, `Do not...`.
    - **Mandatory signs** (Q3): Combine `You must...`, `Please...`, `Gerund + is required`, `Hikers are expected to...`.
    - **Warning signs** (Q4–Q5): Combine `Watch out for...`, `... is dangerous`, `Be careful as...`, `Caution:...`.
    - **Notices, Notes & Emails** (Q6–Q10): Use diverse declarative, modal, passive, and imperative structures.
- **No Automatic Image Generation During Exercise Creation (Không tự động tạo hình ảnh)**:
  - When generating `12_signs_and_notices.json`, write complete, high-quality JSON with structured `sign_text` prompts, but **DO NOT** execute `generate_image` or generate `.png`/`.webp` image files. The user will review the questions in `12_signs_and_notices.json` first and explicitly request image generation later.
- **Standard Concise Question Stems (Không chứa ngữ cảnh chi tiết trong câu hỏi)**:
  - The `question` field MUST be simple, direct, and concise without leaking situational details or clues.
  - For signs (prohibition, mandatory, warning): use `"What does the sign say?"` or `"What does the sign mean?"`.
  - For notices, notes, emails, flyers: use `"What does the notice tell us?"`, `"What does the note say?"`, or `"What does the email say?"`.
  - **DO NOT** embed specific situational context inside the question prompt (e.g., avoid *"What rule must students obey when training on the school running track?"*). The student must interpret the situation entirely from reading the sign/notice itself.
- **Balanced Option Lengths (Cân bằng tương đối độ dài các phương án)**:
  - Keep option lengths roughly balanced so that the correct answer is NOT noticeably longer or shorter than the distractors. This ensures students cannot guess the answer purely based on sentence length or visual cues, while allowing natural, grammatical English sentences without forcing artificial character padding.
- **100% Full-Bleed Square Canvas Fill for Non-Sign Notices (Tận dụng 100% khung ảnh vuông, KHÔNG chừa môi trường thừa)**:
  - When printed on paper or rendered in a small 4cm x 4cm book component, images MUST maximize every square millimeter so that text and icons are 100% legible.
  - For Q6–Q10 (notices, sticky notes, announcements, ads, flyers), the notice card / poster / flyer / paper note ITSELF **MUST fill the entire square image canvas from edge to edge (100% full-bleed layout)**.
  - **DO NOT** render surrounding environments like floating tablets, surrounding wooden doors, corkboard walls, or outer desks that waste canvas space.
  - Prompts MUST explicitly specify: `"Full-bleed square graphic design, 100% edge-to-edge layout filling the entire square image canvas with zero outer background margins, no floating devices or walls, large high-contrast typography, maximum readability when printed."`
- **Uniform Sign Diameter & Scaling for Traffic/Safety Signs (Đường kính biển báo đồng bộ 100%)**:
  - For standard circular prohibition signs and triangular warning signs (Q1–Q5), the sign shape MUST be centered on a plain white background with **identical uniform scale (filling exactly 90% of the square canvas)** and uniform margin padding on all 4 sides. All sign images in an exercise set MUST look 100% uniform, consistent, and visually aligned when rendered next to each other on printed book pages.
  - Circular & triangular signs MUST NOT have any added outer border frame around the image canvas (`NO outer border frame, NO inner border box`).
  - **Icon Accuracy**: Icons inside prohibition signs MUST accurately depict the forbidden action (e.g. *"No littering"* shows crumpled paper falling on the ground with a red slash — NOT a trash bin with trash being thrown inside).
- **Authentic Material & Rich Graphic Textures (Chất liệu thật & họa tiết sinh động)**:
  - Use rich, authentic paper/canvas/metallic textures and vibrant colors directly on the full-bleed card layout (e.g., yellow sticky note paper texture filling the square, dark metallic plaque texture filling the square, textured cream paper flyer filling the square).
- **Rich Aesthetic Graphic Design & Mixed-Case Typography**:
  - **Professional Graphic Quality**: Signs, notices, emails, ads, and flyers MUST feature attractive 2D graphic design (stylish header banners, clean vector illustrations/icons, harmonious colors) so that images look modern, rich, and visually appealing.
  - **Proper Mixed-Case Capitalization (Không dùng ALL-CAPS cả đoạn)**: Use Title Case for headlines/banners (e.g. `'Sports World Sale'`, `'Junior Chess Tournament'`), and standard Sentence Case / mixed-case for message body text (e.g. `'Dear members, the annual football tournament moves to...'`). **DO NOT** write entire long paragraphs in ALL-CAPS, as ALL-CAPS walls of text cause visual fatigue and look messy.
  - For symbol-only signs (Q1–Q5), explicitly append `"NO text or words of any kind."` to prevent AI gibberish text.

When you write `sign_text`, specify a clean 2D description: for signs (Q1–Q5) use clean white background with centered symbols filling exactly 90% of the frame with no added outer borders (`NO outer border frame, NO inner border box`). For non-sign notices (Q6–Q10), specify 100% full-bleed edge-to-edge layouts with rich material textures, large bold typography, zero wasted margin space, and roughly balanced option lengths. The result MUST be flat, beautiful, challenging, and 100% readable when printed.


### Exercise 13 — Word Families Table (up to 10 rows)

For each row, pick a base word **as it appears in `vocab.json`** and fill in every existing form across verb / noun / adjective / adverb columns. 
Rules:
- **Strictly include ONLY common, natural, high-frequency word forms suitable for Grade 6–7 students.**
- **STRICTLY OMIT rare, obscure, archaic, or dictionary-only forms** (e.g., omit `deliciousness`, `deliciously`, `cleanliness`, `cleanly`, `famously`, `excitingly`, `friendlily`). If a word form is uncommon or awkward in everyday English, leave that column array empty `[]`.
- Put a maximum of 2 words per cell (box) to avoid student overload.
- Avoid negative prefixes (like `un-`, `ir-`, `im-`, `in-`) unless they are extremely common and standard (like `unhappy` or `impatient`).
- Use empty array `[]` (NEVER `null`) for forms that don't exist or are uncommon. The frontend Rust parser requires a valid JSON array `[]` to deserialize table questions properly. The `base_word_type` field tells the frontend which column to show as the prompt — it doesn't have to be the verb form.

### Exercise 14 — Word Families MCQ (10)

10 multiple-choice questions testing the forms introduced in exercise 13. Each question uses one word family — don't mix forms from different families inside a single set of options.
- **Strict Active Voice Grammar Ceiling**: All sentences MUST use active voice (Present Simple, Past Simple, Present Continuous, Future Simple, Modals like `can/must/should`). **STRICTLY DO NOT use passive voice** (e.g. `was prepared by`, `is built by`) because Grade 6–7 students have not learned passive voice yet.

### Exercise 15 — Word Formation (5)

5 fill-in-the-blank questions requiring students to supply the correct form of a given base word in brackets.
- **Strict Active Voice**: Sentences MUST use active voice and stay strictly within the target Grade's grammar ceiling.
- **Clear Word Transformation**: Ensure the target answer requires a clear morphological transformation from the base word (e.g. `BEAUTY` $\rightarrow$ `beautiful`, `FRIEND` $\rightarrow$ `friendly`). Avoid cases where the base word and target form are identical.

### Exercise 16 — Translate Sentences (10)

10 Vietnamese sentences with English translations that use Unit vocabulary. The grammar of the English translation must stay within the Unit's grammar ceiling.
