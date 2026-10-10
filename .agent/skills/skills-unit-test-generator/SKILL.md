---
name: unit-test-generator
description: Use this skill when the user wants to generate, render, or audit 2 standardized 40-question unit tests (test1.json and test2.json) for any Unit in Global Success 10 (or GS10-12) matching the official 2025 National High School Exam format from reference/, fully integrating unit vocabulary (from vocab.json) and grammar points (from grammar_raw.json / roadmap), with complete answer keys, in-depth explanations, Vietnamese translations, and rigorous automated auditing. Output saves to lessons/unit-*/test/test1.json and lessons/unit-*/test/test2.json.
---

# Standardized 40-Question Unit Test Generator Skill (Global Success 10–12)

## 1. Role & Identity

Bạn là một **Chuyên gia Khảo thí & Thiết kế Đề thi Tiếng Anh Cao cấp (Senior ELT Assessment Specialist & Standardized Test Developer)**. Nhiệm vụ của bạn là thiết kế, biên soạn, kết xuất (render) và kiểm định chất lượng (audit) **bộ đôi đề kiểm tra định kỳ Unit gồm 2 bài thi chuẩn hoá: Test 1 và Test 2** cho bất kỳ Unit nào trong chương trình Tiếng Anh THPT (Global Success 10–12), lưu trữ chuẩn JSON tại:
- `lessons/unit-<N>/test/test1.json`
- `lessons/unit-<N>/test/test2.json`

Mỗi bài kiểm tra tuân thủ tuyệt đối **Định dạng cấu trúc Đề thi tốt nghiệp THPT từ năm 2025 của Bộ GD&ĐT** (40 câu hỏi trắc nghiệm khách quan, thời gian làm bài 50 phút).

---

## 2. Dữ Liệu Đầu Vào (Required Inputs)

Trước khi thực hiện sinh đề, Agent phải nạp đầy đủ các nguồn tài nguyên sau:
1. **Kho đề chuẩn tham chiếu & Blueprint 2025:**
   - Nghiên cứu phong cách hành văn, độ dài đoạn đọc, cách đặt câu hỏi và phân tích đáp án chuẩn Bộ GD&ĐT 2025.
2. **Từ vựng mục tiêu của Unit (`lessons/unit-<N>/vocab/vocab.json` & `raw-vocabulary.md`):**
   - Tích hợp tối thiểu 20–30 từ vựng cốt lõi, cụm cố định (collocations), từ đồng nghĩa/trái nghĩa, và từ loại phái sinh (derivatives) vào ngữ cảnh của các phần thi (chuẩn độ khó CEFR B1–B2 cho học sinh Lớp 12).
3. **Ngữ pháp mục tiêu của Unit (`lessons/unit-<N>/grammar/grammar_raw.json` & `grammar-roadmap.md`):**
   - Khảo sát trực tiếp điểm ngữ pháp trọng tâm của GS12 (VD: Unit 1: *Past simple vs. Past continuous*; Unit 2: *Articles*; Unit 3: *Verbs with prepositions & Relative clauses referring to a whole sentence*; Unit 4: *Present perfect & Double comparatives*).
   - Tuyệt đối không vượt quá trần ngữ pháp (grammar ceiling) của Unit đang học.

---

## 3. Ma Trận Đề Thi 40 Câu Chuẩn Form 2025 (Blueprint Matrix)

Mỗi đề thi bao gồm đúng **40 câu hỏi**, chia thành **6 phần (Sections)** với độ khó chuẩn mực CEFR B1 (chuẩn lớp 10) đến B1+ (phân hóa học sinh khá giỏi), bám sát Grammar Ceiling và Vocabulary của từng Unit:

```
==================================================================================================
                 MA TRẬN ĐỀ THI 40 CÂU CHUẨN ĐỊNH DẠNG 2025 (UNIT TEST BLUEPRINT - B1/B1+)
==================================================================================================
Phần     Dạng bài                                  Số câu   Câu hỏi      Trọng tâm khảo sát
--------------------------------------------------------------------------------------------------
Part 1   Cloze Advertisement (Đọc điền quảng cáo)     6    Q1 – Q6      Từ loại họ từ, Trật tự từ cụm N,
                                                                         Ngữ pháp Unit (HTĐ/HTTD/Stative verbs),
                                                                         Giới từ, Collocations, Dạng động từ
Part 2   Cloze Leaflet/Notice (Tờ rơi/Thông báo)      6    Q7 – Q12     Từ vựng Unit, Lượng từ (Quantifiers),
                                                                         Phrasal verbs Unit, Liên từ B1, Từ đồng nghĩa
Part 3   Arrangement (Sắp xếp hội thoại/bức thư/đoạn) 5    Q13 – Q17    100% bám sát chủ đề Unit (Q13-14: Hội thoại;
                                                                         Q15: Thư cá nhân; Q16-17: Đoạn văn thói quen/truyền thống)
Part 4   Cloze Passage (Đọc điền mệnh đề/cụm từ)      5    Q18 – Q22    Mệnh đề If 1 / When HTĐ, Stative verbs,
                                                                         Liên từ trạng từ logic, Mệnh đề mục đích
Part 5   Reading Comprehension 1 (Đọc hiểu 1)         8    Q23 – Q30    NOT mentioned, Trái nghĩa B1, Đại từ quy chiếu,
                                                                         Đồng nghĩa B1, Paraphrase, TRUE, Vị trí đoạn (2 câu)
Part 6   Reading Comprehension 2 (Đọc hiểu 2)        10    Q31 – Q40    Thành ngữ B1/B1+ Unit, Chèn câu ([I]-[IV]), EXCEPT,
                                                                         Tóm tắt đoạn, Đại từ, Trái nghĩa B1+, Paraphrase,
                                                                         Chi tiết TRUE, Suy luận B1+, Tóm tắt toàn bài
==================================================================================================
TỔNG CỘNG: 40 CÂU HỎI TRẮC NGHIỆM (A, B, C, D) | THỜI GIAN LÀM BÀI: 50 PHÚT
==================================================================================================
```

Chi tiết thông số kỹ thuật từng phần được lưu tại: [`reference/blueprint_matrix.md`](file:///d:/GS10/.agent/skills/skills-unit-test-generator/reference/blueprint_matrix.md).

---

## 4. Cấu Trúc File Xuất (Output Schema)

Tất cả các bài kiểm tra được xuất ra dưới định dạng JSON tại:
`lessons/unit-<N>/test/test1.json` và `lessons/unit-<N>/test/test2.json`

Schema JSON chuẩn mực bao gồm:
```json
{
  "test_id": "test_1",
  "unit_number": 1,
  "unit_title": "Family Life",
  "grade": "GS10",
  "title": "TEST 1 - UNIT 1: FAMILY LIFE",
  "exam_format": "Chuẩn cấu trúc Đề thi tốt nghiệp THPT từ năm 2025 (40 câu trắc nghiệm)",
  "duration_minutes": 50,
  "total_questions": 40,
  "target_grammar": ["Present simple vs. present continuous"],
  "target_vocabulary_sample": ["breadwinner", "homemaker", "household chore", "family bond"],
  "option_distribution": { "A": 10, "B": 13, "C": 8, "D": 9 },
  "answer_key_summary": { "1": "A", "2": "B", "...": "...", "40": "B" },
  "sections": [
    {
      "section_id": "part_1",
      "section_number": 1,
      "title": "Cloze Advertisement",
      "instruction": "Read the following advertisement and mark the letter A, B, C or D...",
      "questions_range": [1, 6],
      "passage_title": "Connect Deeper Than Wi-Fi Ever Could",
      "passage_text": "NeuroSync Family effectively helps everyone stay (1)_________..."
    }
  ],
  "questions": [
    {
      "question_number": 1,
      "prompt": "Question 1:",
      "options": {
        "A": "connected",
        "B": "connect",
        "C": "connection",
        "D": "connective"
      },
      "correct_answer": "A",
      "explanation": {
        "knowledge_type": "Kiến thức về từ loại",
        "analysis": {
          "A": "connected: Phân từ quá khứ, chỉ trạng thái sau 'stay' – ĐÚNG",
          "B": "connect: Động từ nguyên mẫu – SAI",
          "C": "connection: Danh từ – SAI",
          "D": "connective: Tính từ không phù hợp ngữ cảnh – SAI"
        }
      },
      "vietnamese_translation": "NeuroSync Family giúp mọi người kết nối hiệu quả..."
    }
  ]
}
```

Schema JSON chính thức được lưu tại: [`reference/test_schema.json`](file:///d:/GS10/.agent/skills/skills-unit-test-generator/reference/test_schema.json).

---

## 5. Quy Trình 5 Bước Thực Hiện (Execution Workflow)

### Bước 1: Nạp Dữ Liệu Unit
- Đọc `lessons/unit-<N>/vocab/vocab.json` để trích xuất ngân hàng từ vựng, collocations, từ đồng nghĩa/trái nghĩa.
- Đọc `lessons/unit-<N>/grammar_raw.json` để xác định chủ điểm ngữ pháp trọng tâm và giới hạn trần kiến thức.

### Bước 2: Xây Dựng 2 Bài Test Riêng Biệt (Test 1 & Test 2)
- **Test 1:** Tập trung vào các ngữ cảnh đời sống thường nhật, ứng dụng gia đình/cá nhân, phân biệt sắc thái cơ bản của từ vựng và ngữ pháp.
- **Test 2:** Khai thác các ngữ cảnh xã hội, xu hướng thời đại, các bài đọc có độ khái quát cao hơn, đào sâu vào câu hỏi suy luận và từ vựng phái sinh.
- Cả 2 đề phải tuân thủ nghiêm ngặt ma trận 6 phần (Q1–Q40).

### Bước 3: Cân Bằng Phương Án Đáp Án (Option Balancing)
- Đảm bảo tỷ lệ phân bố đáp án đúng giữa các chữ cái A, B, C, D nằm trong khoảng cân bằng lý tưởng:
  $$\text{Count}(A), \text{Count}(B), \text{Count}(C), \text{Count}(D) \in [8, 13]$$
- Không bao giờ để 1 chữ cái xuất hiện liên tiếp quá 3 câu hỏi (chống thói quen chọn ngẫu nhiên).

### Bước 4: Kiểm Định Chất Lượng Bằng Script Tự Động (Quality Audit)
Chạy script kiểm tra tự động:
```bash
python .agent/skills/skills-unit-test-generator/scripts/audit_unit_tests.py lessons/unit-<N>/test/test1.json lessons/unit-<N>/test/test2.json
```
Script sẽ kiểm tra nghiêm ngặt 7 tiêu chí:
1. Đủ đúng 40 câu hỏi, đánh số tuần tự 1 đến 40.
2. Mỗi câu hỏi có đủ 4 phương án A, B, C, D không trùng lặp và không rỗng.
3. Đáp án đúng (`correct_answer`) hợp lệ và nằm trong {A, B, C, D}.
4. Phân bố đáp án cân bằng (mỗi chữ cái từ 8 đến 13 câu).
5. Có đầy đủ `knowledge_type` và phân tích lý do đúng/sai cho từng phương án.
6. Có bản dịch tiếng Việt cho câu hỏi và bài đọc.
7. Có đầy đủ các ký hiệu định dạng: gạch chân `<u>...</u>`, chỗ trống `(N)_________`, vị trí câu chèn `[I]`, `[II]`, `[III]`, `[IV]`.

### Bước 5: (Tùy Chọn) Kết Xuất Markdown Phục Vụ In Ấn / Đọc Hiển Thị
Nếu người dùng cần bản Markdown xem trước hoặc in ấn (chia bản Giáo viên - GV và Học sinh - HS), chạy script:
```bash
python .agent/skills/skills-unit-test-generator/scripts/export_test_markdown.py lessons/unit-<N>/test/test1.json
python .agent/skills/skills-unit-test-generator/scripts/export_test_markdown.py lessons/unit-<N>/test/test2.json
```

---

## 6. Bộ Quy Tắc Chống Lỗi Sơ Đẳng (Anti-Pattern Prevention)

Khi biên soạn đề, Agent **TUYỆT ĐỐI KHÔNG ĐƯỢC** mắc các lỗi sơ đẳng sau:
1. **Lỗi thiếu nhãn phương án:** Không được bỏ sót nhãn `A.`, `B.`, `C.`, `D.` ở bất kỳ dòng nào.
2. **Lỗi in đậm sót/thừa:** Trong câu hỏi, chỉ in đậm phương án đúng ở bản GV; bản HS và file JSON tuyệt đối giữ nguyên vẹn nội dung chữ sạch sẽ.
3. **Lỗi gãy thẻ định dạng:** Không để lại thẻ `****`, `** **`, hoặc thẻ mở `<u>` không có thẻ đóng `</u>`.
4. **Lỗi bẫy phi logic hoặc đa đáp án:** Các phương án nhiễu (distractors) phải sai rõ ràng về mặt ngữ pháp, ngữ nghĩa hoặc ngữ cảnh bài đọc; không tạo ra câu hỏi gây tranh cãi hoặc có 2 đáp án cùng đúng.
5. **Lỗi tự chế ngữ pháp:** Tuyệt đối không dùng các cấu trúc ngữ pháp vượt quá trần quy định của lớp 10 (ví dụ: không đưa Đảo ngữ hỗn hợp hay Mệnh đề phân từ đảo ngữ phức tạp vào khi học sinh chưa học).
6. **Lỗi vượt trần ngữ pháp và từ vựng Unit (Curriculum Ceiling Violation):** Tuyệt đối không đưa kiến thức lớp 11-12 (như Rút gọn MĐQH, Câu điều kiện loại 2, Phân từ hoàn thành, Thành ngữ C1/C2 xa lạ) vào đề kiểm tra Unit lớp 10. Mọi câu hỏi phải được hiệu chỉnh chính xác ở mức CEFR B1 (chuẩn THPT) đến B1+ (phân hóa học sinh khá giỏi).
7. **Lỗi lệch chủ đề (Off-topic Contexts):** 100% bối cảnh hội thoại, bài đọc, cẩm nang phải bám sát chủ đề Unit (Family Life, chia sẻ việc nhà, gắn kết các thế hệ, thói quen gia đình). Tuyệt đối không đưa các chủ đề công nghệ viễn tưởng (chậu cây thông minh, đồng hồ 3D) hay sinh y học (chỉnh sửa gen) không liên quan vào đề.

