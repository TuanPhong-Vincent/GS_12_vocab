---
name: vocab-60min-lesson
description: Use this skill when the user wants to design, generate, or deliver an intensive, highly effective 60-minute English vocabulary lesson for any Unit in Global Success 12 (GS12) based on Paul Nation's Four Strands, Michael Lewis's Lexical Approach, Craik & Lockhart / Laufer's Task Involvement Load, Pimsleur Spaced Retrieval, and the 10 Golden Rules. It provides the complete 60-minute pedagogical delivery rules, cognitive stage breakdowns, activity banks mapped to the 16 exercise JSONs, and generates publication-grade lesson plans in Markdown and HTML.
---

# 60-Minute Master Vocabulary Lesson Delivery Skill (`vocab-60min-lesson`)

## 1. Vai Trò & Nền Tảng Sư Phạm Cốt Lõi (Role & Pedagogical Foundations)

Bạn là một **Chuyên gia Sư phạm Giảng dạy Tiếng Anh Cao cấp & Kỹ sư Thiết kế Bài giảng (Senior ELT Pedagogy Specialist & Instructional Designer)**. Nhiệm vụ của bạn là thiết kế một tiến trình giảng dạy tiết học từ vựng 60 phút hoàn chỉnh, chi tiết, đo lường được và đạt hiệu quả tối ưu cho học sinh THPT (Global Success 12).

Toàn bộ tiết học được neo chặt vào các cột trụ khoa học:
1. **Paul Nation (Four Strands & 9 Facets Matrix):** Cân bằng 4 nhánh (Input, Output, Language Learning, Fluency); bao quát cả 3 trục *Hình thái (Form)* - *Ý nghĩa (Meaning)* - *Cách dùng (Use)*.
2. **Michael Lewis (The Lexical Approach):** *"Language consists of grammaticalised lexis, not lexicalised grammar."* Đơn vị giảng dạy không phải từ đơn lẻ mà là **Khối ngữ lưu (Lexical Chunks)** và kết hợp từ (*Collocations*).
3. **Craik & Lockhart & Laufer & Hulstijn (Cognitive Depth & Involvement Load):** Nâng dần chỉ số tải trọng tác vụ qua công thức $\text{Involvement Load} = \text{Need} + \text{Search} + \text{Evaluation}$ từ mức 1–2 lên mức 5 (Mức sản sinh sâu).
4. **Hermann Ebbinghaus & Paul Pimsleur (Spaced Retrieval):** Đánh bại đường cong quên lãng bằng hoạt động truy hồi chủ động (*Active Recall*) và thiết lập cam kết lặp lại 24h & 7 ngày.

---

## 2. Nguồn Dữ Liệu Đầu Vào (Target Input Assets)

Khi triển khai cho bất kỳ Unit nào (ví dụ: `lessons/unit-1/vocab` hoặc `unit-[X]/vocab`):
1. **Lý thuyết & Thẻ từ vựng:**
   - `vocab.json`: Chứa dữ liệu ngữ âm, từ loại, định nghĩa, câu ví dụ, collocations, audio và hình ảnh minh họa.
   - `cards.html`: Giao diện flashcard trực quan chuẩn mực (Modern Blue, audio button, contain image frame).
2. **Kho bài tập 16 dạng chuẩn hóa (`exercises/*.json`):**
   - Từ `01_multiple_choice_direct.json` đến `16_translate_sentences.json`.
3. **Văn bản ngữ cảnh gốc:**
   - `raw-content.md` và `raw-vocabulary.md`.

---

## 3. Bộ 10 Quy Tắc Vàng Giảng Dạy Tiết Học 60 Phút (Mandatory Rules)

Giáo viên và AI khi thiết kế hoặc đứng lớp **bắt buộc tuân thủ nghiêm ngặt 10 quy tắc sau**:

### Rule 1: Quy tắc "Collocation First" (Michael Lewis)
- **Tuyệt đối cấm dạy từ đơn lẻ cô lập (Isolated Word).**
- Mọi danh từ phải đi kèm động từ/tính từ đối tác (ví dụ: dạy *do the heavy lifting*, *share housework*, *primary breadwinner*; không bao giờ chỉ viết *lifting* hay *breadwinner* trơ trọi).
- Sử dụng sơ đồ **Collocation Grid 5-5-1** (5 Động từ + 5 Tính từ ghép với 1 Danh từ trung tâm).

### Rule 2: Quy tắc 4 Bước Trình Chiếu Chuẩn (Meaning First)
- Cấm đưa mặt chữ ra trước khi học sinh nắm nghĩa và âm thanh.
- Thứ tự chuẩn: **Ý nghĩa (Meaning) $\rightarrow$ Âm thanh (Spoken Form) $\rightarrow$ Chữ viết (Written Form) $\rightarrow$ Kết hợp & Cá nhân hóa (Collocation & Personalisation)**.

### Rule 3: Quy tắc 80/20 & Quản lý Tải trọng Nhận thức (Cognitive Load)
- Trong 60 phút, **chỉ chọn 8–10 Target Lexical Chunks cốt lõi** để khai thác sâu ở mức sản sinh chủ động (Productive).
- Các từ còn lại được xếp vào nhóm thụ nhận (Receptive) thông qua bài đọc, bài tập điền từ hoặc giao về nhà tự ôn.

### Rule 4: Quy tắc Chống Nhiễm Chéo Ngữ Nghĩa (Delay Semantic Foes)
- Tuân thủ nghiên cứu của Tinkham & Waring: **Không bao giờ dạy cùng lúc hai từ trái nghĩa trực tiếp hoặc từ đồng vị dễ nhầm trong cùng một slide/hoạt động** (ví dụ: *breadwinner* vs. *homemaker*; *hot* vs. *cold*).
- Dạy từ có tần suất cao trước (*deep*); từ đối ứng chỉ giới thiệu sau khi từ gốc đã định hình vững chắc trong não bộ.

### Rule 5: Quy tắc "Đọc bằng Tai" & Kỹ thuật Mumble Drill
- Khắc phục **Hiệu ứng bồn tắm (The Bathtub Effect)**: Khi học sinh ngập ngừng, giáo viên gõ nhịp trọng âm hoặc gợi ý âm tiết giữa, không chỉ mớm chữ cái đầu.
- Khi luyện phát âm: Luôn cho học sinh **3 giây tự nhẩm trong miệng (Mumble Drill)** để tạo âm thanh nội tâm trước khi đọc đồng thanh (Choral) và cá nhân (Individual).

### Rule 6: Quy tắc Thang bậc Nhận thức Tịnh tiến (Cognitive Hierarchy)
- Tiến trình bài tập phải đi theo đường dẫn nhận thức:
  $$\text{Identifying (Nhận diện)} \longrightarrow \text{Selecting (Lựa chọn)} \longrightarrow \text{Sorting (Phân loại họ từ)} \longrightarrow \text{Production (Sản sinh)}$$
- Tăng dần chỉ số Involvement Load từ $1-2$ (nhận biết) lên $5$ (tự sáng tạo câu giao tiếp).

### Rule 7: Quy tắc Cân Bằng 4 Nhánh (The Four Strands Ratio)
- Phân bổ 60 phút đảm bảo:
  - *Language-focused Learning (25-30% ~ 18p):* Dạy trực tiếp Form, Meaning, Pronunciation.
  - *Controlled Practice (25% ~ 15p):* Thao tác nhận diện, ghép nối, họ từ.
  - *Meaning-focused Output & Fluency (25% ~ 14p):* Nói, viết, đối thoại giải quyết tình huống thật.
  - *Warm-up & Assessment (15-20% ~ 13p):* Khởi động, truy hồi lặp lại giãn cách và Exit Ticket.

### Rule 8: Quy tắc Dịch theo Khối Tương Đương (Chunk-for-Chunk)
- Tuyệt đối cấm lối dịch thô word-by-word từng từ đơn lẻ.
- Khi chữa bài tập dịch (`16_translate_sentences.json`), luôn yêu cầu học sinh khoanh vùng cụm tiếng Việt tương đương khối tiếng Anh (*"gánh vác việc nhà"* $\leftrightarrow$ *"handle household chores"*).

### Rule 9: Quy tắc Sửa Lỗi Trì Hoãn Trong Giao Tiếp (Delayed Feedback)
- Khi học sinh đang luyện nói lưu loát ở Giai đoạn 4, giáo viên **không được ngắt lời để bắt lỗi ngữ pháp nhỏ**.
- Giáo viên ghi chép lỗi phát âm/collocation vào sổ tay sư phạm và dành 2 phút cuối hoạt động để phản hồi chung trước cả lớp (Praise first, correct after).

### Rule 10: Quy tắc Cam Kết Lặp Lại Giãn Cách (Spaced Retrieval Contract)
- Mọi tiết học đều phải kết thúc bằng **Exit Ticket 3-2-1** để kiểm tra mức độ lưu giữ (VKS Levels 4-5).
- Thiết lập hợp đồng tự học: Mở `cards.html` (che nghĩa) sau 24h và làm bài kiểm tra trên `index.html` sau 7 ngày.

---

## 4. Khung Tiến Trình Chi Tiết Toàn Bộ Buổi Học 60 Phút (60-Minute Master Schedule)

```
========================================================================================
                          TIMELINE TIẾT HỌC 60 PHÚT
========================================================================================
### Sơ Đồ Phân Bổ Bảng Lớp Học (Board Layout Blueprint - 3 Cột Suốt 60 Phút)
```
+---------------------------+-----------------------------------+-----------------------------+
| CỘT TRÁI (LƯU ĐỘNG)       | CỘT GIỮA (TRỌNG TÂM DÀI HẠN)      | CỘT PHẢI (NHIỆM VỤ & QUẢN LÝ)|
| - Odd-One-Out Blitz       | UNIT [X]: [TÊN UNIT] - LEXIS      | - Timeline 60p (5 Stages)   |
| - Spelling Traps:         | 1. Collocation Grid 5-5-1:        | - Bảng điểm thi đua nhóm    |
|   breadwinner (double n)  |    [sole / primary] + BREADWINNER | - Khung Cascade 3 Lượt:     |
| - Delayed Feedback Board: |    [do / share] + HOUSEWORK       |   A: Initiator              |
|   (make a decision)       | 2. Sentence Frame:                |   B: I-focus                |
|                           |    "In my family, ... while ..."  |   A: You-focus              |
|                           | 3. Word Family Matrix:            | - Exit Ticket 3-2-1 Prompt  |
|                           |    support -> supporter -> ...    | - Hợp đồng Pimsleur 24h & 7d|
+---------------------------+-----------------------------------+-----------------------------+
```

> **YÊU CẦU TIÊU CHUẨN SƯ PHẠM VI MÔ (MICRO-SCRIPTED STANDARD):**
> Mọi kế hoạch bài dạy sinh ra từ skill này **BẮT BUỘC** phải có:
> 1. **Lời nói nguyên văn của Giáo viên (Teacher Talk Verbatim):** Từng câu lệnh, câu chào, câu CCQ, câu khen ngợi cụ thể bằng tiếng Anh và tiếng Việt.
> 2. **Cử chỉ & Ngôn ngữ cơ thể (Body Language & Physical Gestures):** Đứng ở đâu, tay chỉ thế nào, biểu cảm nét mặt ra sao, cử chỉ ra hiệu lắng nghe/im lặng.
> 3. **Hành vi cụ thể của Học viên (Student Actions):** Viết gì, giơ bảng thế nào, thảo luận cặp ra sao, lời thoại của học sinh mẫu.
> 4. **Trình tự sắp xếp lớp học:** Bàn ghế, thiết bị trình chiếu, tài liệu trên bàn học sinh từ trước giờ học (T-5 phút).

---

### GIAI ĐOẠN 1: WARM-UP & SPACED RETRIEVAL (00:00 - 00:07 | 7 PHÚT)
- **Mục tiêu nhận thức:** Kích hoạt mạng lưới ngữ nghĩa (*Spreading Activation*), thực hiện lặp lại giãn cách (*Active Recall* kiến thức bài trước theo Pimsleur), dẫn nhập bối cảnh bài học.
- **Chỉ số Tác vụ:** Involvement Load = 2 (Need = 1, Search = 0, Evaluation = 1).
- **Hoạt động cụ thể:**
  1. *Hoạt động 1.1: Odd-One-Out Collocation Blitz (3 phút):*
     - Giáo viên chiếu 3 nhóm kết hợp từ lên bảng (ví dụ: `do` + *chores / housework / the cooking / \*a decision*).
     - Học sinh có 15 giây viết từ kết hợp sai lên bảng con (Mini-whiteboard) và đồng loạt giơ lên khi có hiệu lệnh.
     - Giáo viên gọi 1 học sinh giải thích cụm đúng (*make a decision*).
  2. *Hoạt động 1.2: Visual Thematic Hook (4 phút):*
     - Chiếu 2 bức tranh đại diện từ `cards.html` hoặc `04_pic_to_word.json`.
     - Giáo viên đặt câu hỏi dẫn dắt (Teacher Talk): *"Look at Picture A and B. What roles do you see? Who brings the main income, and who handles domestic chores? Today, we will master the powerful lexical chunks to discuss..."*

---

### GIAI ĐOẠN 2: LANGUAGE-FOCUSED LEARNING - 4 BƯỚC KHẮC SÂU CHUNKS (00:07 - 00:25 | 18 PHÚT)
- **Mục tiêu nhận thức:** Chiếm lĩnh 8–10 Target Lexical Chunks theo ma trận 9 khía cạnh (Paul Nation). Loại bỏ Bathtub Effect và hiện tượng dịch thô.
- **Chỉ số Tác vụ:** Involvement Load = 3 (Need = 1, Search = 0, Evaluation = 2).
- **Tiến trình 4 bước sư phạm chuẩn:**
  1. *Bước 1: Xác lập Ý nghĩa (Meaning First - 4 phút):*
     - Dùng hình ảnh trực quan từ `cards.html` và định nghĩa súc tích (*Defining Vocabulary*).
     - Đặt câu hỏi kiểm tra khái niệm (**CCQs - Concept Checking Questions**):
       - *Ví dụ với chunk "breadwinner":*
         - *"Does a breadwinner stay home all day or work to earn money?"* $\rightarrow$ *Work to earn money.*
         - *"Can a woman be a breadwinner?"* $\rightarrow$ *Yes, absolutely.*
  2. *Bước 2: Khắc sâu Âm thanh (Spoken Form & Mumble Drill - 5 phút):*
     - Giáo viên phát âm mẫu chuẩn 2 lần (hoặc phát audio từ `cards.html`).
     - Yêu cầu học sinh thực hiện **Mumble Drill (3 giây tự nhẩm)** trong tâm trí mà không phát ra tiếng.
     - Đọc đồng thanh (Choral) theo nhịp gõ trọng âm $\rightarrow$ Gọi cá nhân (Individual) 3 học sinh để chỉnh sửa âm cuối và trọng âm.
  3. *Bước 3: Khắc sâu Chữ viết & Cảnh báo Bẫy Chính tả (Written Form - 4 phút):*
     - Chiếu mặt chữ trên slide. Dùng màu đỏ/vàng làm nổi bật các bẫy chính tả (*Spelling Traps*): phụ âm đôi (*breadwi**nn**er*, *ho**mm**aker*), chữ cái câm (*dou**b**t*).
     - Học sinh ghi nhanh vào sổ tay từ vựng theo mẫu.
  4. *Bước 4: Kết hợp từ & Cá nhân hóa (Collocation & Personalisation - 5 phút):*
     - Giáo viên dựng sơ đồ **5-5-1 Collocation Grid** trên bảng.
     - Cho học sinh 1 phút hoàn thành câu thật về cuộc sống của mình theo khung câu (*Sentence Frame*):
       - *"In my family, [person] is the primary breadwinner, while I usually help with [chore]."*
     - Mời 2 học sinh chia sẻ trước lớp (*Affective Depth*).

---

### GIAI ĐOẠN 3: CONTROLLED PRACTICE - THANG BẬC NHẬN THỨC (00:25 - 00:40 | 15 PHÚT)
- **Mục tiêu nhận thức:** Chuyển dịch nhận thức qua các nấc thang: Nhận diện (*Identifying*) $\rightarrow$ Lựa chọn (*Selecting*) $\rightarrow$ Phân loại họ từ (*Sorting*).
- **Chỉ số Tác vụ:** Involvement Load = 3–4 (Need = 2, Search = 0, Evaluation = 1–2).
- **Hoạt động cụ thể trích xuất từ 16 bài tập:**
  1. *Hoạt động 3.1: Speed Collocation & Sentence Fill (6 phút):*
     - Trích xuất 4 câu trắc nghiệm ngữ cảnh từ `02_multiple_choice_sentence.json` hoặc `06_fill_in_blanks.json`.
     - Học sinh thảo luận theo cặp (*Think-Pair-Share*) trong 45 giây.
     - Bắt buộc học sinh gạch chân **"Từ đối tác" (Collocation Clue)** trong đề trước khi đưa ra đáp án cuối cùng.
  2. *Hoạt động 3.2: Morphology & Word Family Matrix (5 phút):*
     - Khai thác bảng họ từ từ `13_word_families_table.json` và 2 câu biến đổi từ `15_word_formation.json`.
     - Phân tích cấu trúc hậu tố (-er, -ment, -tion, -ful) để giảm tải ghi nhớ dài hạn theo nguyên lý Word Family.
  3. *Hoạt động 3.3: Real-World Pragmatics / Signs & Notices (4 phút):*
     - Khai thác 2 tình huống từ `12_signs_and_notices.json`.
     - Học sinh phân tích ngữ cảnh: Biển báo/thông báo này đặt ở đâu, có ý nghĩa gì trong đời thực.

---

### GIAI ĐOẠN 4: MEANING-FOCUSED OUTPUT & COMMUNICATIVE FLUENCY (00:40 - 00:54 | 14 PHÚT)
- **Mục tiêu nhận thức:** Đạt đỉnh tháp nhận thức Mức 3 (Involvement Load = 5: Need = 2, Search = 1, Evaluation = 2). Chuyển hóa vốn từ từ thụ nhận sang sản sinh tự do và tự động hóa độ lưu loát.
- **Hoạt động cụ thể:**
  1. *Hoạt động 4.1: Cascade 3-Part Exchange (6 phút):*
     - Khai thác dữ liệu từ `03_multiple_choice_conversation.json` để dựng khung tương tác:
       - **Initiator (Khởi xướng):** *"The house is quite untidy today!"*
       - **Response [I-focus]:** *"I know. I'll do the washing-up and take out the rubbish right now."*
       - **Response [You-focus]:** *"Great! Could you help me with the heavy lifting later?"*
     - Cặp học sinh luân phiên đối thoại tự nhiên, mắt nhìn nhau (*Eye contact*), không cầm giấy đọc.
  2. *Hoạt động 4.2: Communicative Task - "1-Minute Fluency Pitch" & Chunk Relay (8 phút):*
     - Khai thác thêm mẫu dịch câu theo khối từ `16_translate_sentences.json`.
     - Nhiệm vụ nhóm 3 người: Lên kế hoạch phân chia việc nhà lý tưởng cho các thành viên trong gia đình.
     - Bắt buộc dùng ít nhất 3 target chunks vừa học.
     - Đại diện 2 nhóm thuyết trình trong 60 giây (*1-Minute Fluency Pitch*). Giáo viên quan sát, ghi nhận lỗi và phản hồi trì hoãn (*Delayed Feedback*).

---

### GIAI ĐOẠN 5: WRAP-UP, ASSESSMENT & SPACED CONTRACT (00:54 - 01:00 | 6 PHÚT)
- **Mục tiêu nhận thức:** Đánh giá quá trình (*Formative Assessment*) theo thang Vocabulary Knowledge Scale (VKS), ngăn ngừa đường cong quên lãng bằng hợp đồng lặp lại giãn cách.
- **Hoạt động cụ thể:**
  1. *Hoạt động 5.1: Exit Ticket 3-2-1 Retrieval Challenge (4 phút):*
     - Học sinh hoàn thành phiếu cá nhân:
       - **3 Chunks:** 3 cụm từ em nhớ nhất và phát âm tự tin nhất hôm nay.
       - **2 Sentences:** 2 câu hoàn chỉnh nói về trải nghiệm thật của bản thân có dùng 2 cụm từ trên.
       - **1 Trap:** 1 bẫy chính tả hoặc phát âm mà em cần đặc biệt cẩn trọng.
     - Thu 100% phiếu tại cửa lớp.
  2. *Hoạt động 5.2: Spaced Retrieval Contract (Lịch Pimsleur) (2 phút):*
     - **Sau 24 giờ (Ngày mai):** Mở `cards.html`, dùng tay che cột nghĩa tiếng Việt, nhìn tranh và nghe audio để tự lực truy hồi (*Active Recall*).
     - **Sau 7 ngày (Buổi học kế tiếp):** Vào `index.html` chọn chế độ **Practice Mode** để làm bài tự kiểm tra 10 câu trắc nghiệm.

---

## 5. Ma Trận Ánh Xạ 16 Dạng Bài Tập Vào 60 Phút

| Giai Đoạn Trong Tiết Học | Dạng Bài Tập Sử Dụng Trực Tiếp | Dạng Bài Tập Giao Về Nhà / Tự Học (Spaced Practice) |
|---|---|---|
| **Giai đoạn 1: Warm-up** | `04_pic_to_word.json`, `09_mcq_closest` / `10_mcq_opposite` (từ bài cũ) | - |
| **Giai đoạn 2: Language-focused** | `cards.html` (Lý thuyết), `vocab.json`, `05_write_english_words.json` | - |
| **Giai đoạn 3: Controlled Practice** | `02_mcq_sentence.json`, `06_fill_in_blanks.json`, `13_word_families_table.json`, `15_word_formation.json`, `12_signs_and_notices.json` | `01_multiple_choice_direct.json`, `07_paragraph_fill.json`, `14_word_families_mcq.json` |
| **Giai đoạn 4: Output & Fluency** | `03_mcq_conversation.json`, `08_sentence_ordering.json`, `16_translate_sentences.json` | `11_dictionary_entry.json` |
| **Giai đoạn 5: Assessment & Spaced** | Phiếu Exit Ticket 3-2-1 | `index.html` (Chế độ Practice Mode trực tuyến) |

---

## 6. Hướng Dẫn Sử Dụng Script Tự Động Hóa (Automation Script)

Để tự động phân tích `vocab.json` và toàn bộ 16 tệp bài tập của bất kỳ Unit nào rồi xuất ra Kế hoạch bài dạy 60 phút hoàn chỉnh (Markdown và HTML trình chiếu/in ấn):

```powershell
python .agent/skills/skills-vocab-60min-lesson/scripts/generate_60min_lesson.py <đường_dẫn_thư_mục_unit_hoặc_vocab>
```

### Ví dụ Thực Thi:
```powershell
# Dành cho Unit 1:
python .agent/skills/skills-vocab-60min-lesson/scripts/generate_60min_lesson.py lessons/unit-1/vocab

# Dành cho Unit 2:
python .agent/skills/skills-vocab-60min-lesson/scripts/generate_60min_lesson.py lessons/unit-2/vocab
```

### Kết quả đầu ra tự động:
- `lessons/unit-[X]/vocab/lesson_plan_60min.md`: Kế hoạch bài dạy dạng Markdown chuẩn bị giáo án cho giáo viên.
- `lessons/unit-[X]/vocab/lesson_plan_60min.html`: Bản thiết kế web tương tác chuẩn in ấn / trình chiếu sang trọng, trực quan.
