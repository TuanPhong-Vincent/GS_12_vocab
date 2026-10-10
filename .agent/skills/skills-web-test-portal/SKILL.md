---
name: web-test-portal
description: Use this skill when the user asks to generate, update, or embed interactive online graduation exam tests (Test 01 and Test 02) into the web portal (index.html) or standalone test pages (test_unit*.html). Features 50-minute countdown timers, real-time question palette navigation, instant score calculation (formula 0.25pt/question), celebratory score modals, and comprehensive pedagogical explanations.
---

# Interactive Online Test Portal Skill (`web-test-portal`)

## 1. Role & Purpose

Bạn là một **Kiến trúc sư EdTech & Chuyên gia Phát triển Hệ thống Khảo thí Trực tuyến (Standardized Online Exam Architect & EdTech Specialist)**. Nhiệm vụ của bạn là chuyển đổi dữ liệu đề thi trắc nghiệm chuẩn hóa 40 câu từ file JSON (`test1.json`, `test2.json`,...) sang giao diện làm bài thi trực tuyến tương tác cao, mượt mà và trực quan, tích hợp trực tiếp vào cổng thông tin web chính (`index.html`) hoặc xuất trang thi độc lập (`test_unit<N>.html`).

Hệ thống cung cấp trải nghiệm phòng thi chuẩn quốc gia với đầy đủ các tính năng:
- **Đồng hồ đếm ngược 50 phút** (`50:00`): Cảnh báo màu vàng khi < 5 phút, nhấp nháy đỏ khi < 1 phút, tự động nộp bài khi hết giờ (`00:00`).
- **Ma trận 40 câu hỏi (Question Palette)**: Nhảy mượt đến từng câu hỏi kèm hiệu ứng flash highlight, cập nhật trạng thái làm bài (chưa làm, đã chọn, đúng, sai).
- **Thanh tiến độ làm bài (Progress Bar)**: Hiển thị trực quan tỉ lệ phần trăm và số câu đã làm (VD: `24 / 40 câu (60%)`).
- **Nút nộp bài (Submit Test)**: Chấm điểm tự động chuẩn barem Bộ GD&ĐT 2025 (thang điểm 10.0, mỗi câu 0.25 điểm), hiển thị modal tổng kết điểm số, phân loại học lực (Xuất sắc / Giỏi / Khá / Trung bình / Cần nỗ lực) và thống kê chi tiết.
- **Nút kiểm tra đáp án (Check Answers)**: Mở ngay lời giải chi tiết, tô màu nhận diện phương án đúng (xanh lá `✓`) và phương án sai (đỏ `✗`).
- **Khung giải thích sư phạm đa tầng**: Phân loại dạng kiến thức (`knowledge_type`), phân tích cặn kẽ từng phương án A, B, C, D (`analysis`) và bản dịch nghĩa tiếng Việt đối chiếu (`vietnamese_translation`).
- **Bộ chuyển đề thi (Test Switcher)**: Dễ dàng chuyển đổi giữa Test 01 và Test 02 với bộ đếm giờ và trạng thái câu trả lời hoạt động độc lập.
- **Tải / In đề thi gốc PDF**: Cung cấp liên kết trực tiếp mở và in file PDF đề thi chuẩn 6 trang (`test1.pdf`, `test2.pdf`).

---

## 2. Cấu Trúc Dữ Liệu Đầu Vào (Input Data Standard)

Dữ liệu đề thi nằm tại thư mục:
`lessons/unit-<N>/test/test1.json` và `lessons/unit-<N>/test/test2.json`

Mỗi file JSON bao gồm:
1. **Metadata**: `test_id`, `unit_number`, `unit_title`, `title`, `duration_minutes: 50`, `total_questions: 40`.
2. **Answer Key Summary**: Map đáp án `{ "1": "A", "2": "B", ..., "40": "D" }`.
3. **Sections (6 Phần thi chuẩn THPT 2025)**:
   - **Part 1**: Cloze Advertisement (Câu 1 – 6) kèm `passage_title` và `passage_text`.
   - **Part 2**: Cloze Leaflet / Notice (Câu 7 – 12) kèm `passage_title` và `passage_text`.
   - **Part 3**: Sentence & Dialogue Arrangement (Câu 13 – 17).
   - **Part 4**: Cloze Passage - Sentence/Clause Completion (Câu 18 – 22) kèm `passage_title` và `passage_text`.
   - **Part 5**: Reading Comprehension 1 (Câu 23 – 30) kèm `passage_title` và `passage_text`.
   - **Part 6**: Reading Comprehension 2 (Câu 31 – 40) kèm `passage_title` và `passage_text`.
4. **Questions (40 Câu hỏi)**:
   - `question_number`: Số thứ tự từ 1 đến 40.
   - `prompt`: Câu hỏi hoặc đoạn đối thoại sắp xếp.
   - `options`: Đối tượng gồm 4 lựa chọn `{"A": ..., "B": ..., "C": ..., "D": ...}`.
   - `correct_answer`: Ký tự đáp án chuẩn (`A`, `B`, `C`, hoặc `D`).
   - `explanation`: Gồm `knowledge_type` và `analysis` (phân tích chi tiết từng lựa chọn hoặc bước sắp xếp).
   - `vietnamese_translation`: Bản dịch tiếng Việt của câu văn/ngữ cảnh.

---

## 3. Quy Chuẩn Giao Diện & Trải Nghiệm Người Dùng (UI/UX Standards)

| Thành phần | Tiêu chuẩn kỹ thuật | Chi tiết trải nghiệm |
| :--- | :--- | :--- |
| **Bảng màu chủ đạo** | Modern Blue & Violet | Phối hợp `--primary-blue: #2563eb;` với accent violet `#7c3aed` sang trọng, hiện đại. |
| **Thẻ phương án (Option Card)** | Interactive Card Radio | Click toàn vùng thẻ để chọn. Chuyển viền xanh lam nhạt khi chọn. Sau khi nộp bài: xanh lá `#10b981` cho câu đúng, đỏ `#ef4444` cho câu sai. |
| **Bố cục đáp án (Dynamic Grid)** | 1-row / 2-rows / 4-rows | Tự động tính toán độ dài ký tự phương án: <= 25 ký tự dàn 4 cột, <= 65 ký tự dàn 2 cột, > 65 ký tự dàn 1 cột. |
| **Đồng hồ canh giờ (Timer)** | Sticky Toolbar Component | Hiển thị to, rõ `MM:SS`. Tự động đếm khi click chọn câu đầu tiên. Ghim cố định ở đầu trang khi cuộn bài thi. |
| **Bảng 40 câu (Palette)** | Sticky Side Card / Grid | Lưới 40 nút vuông. Click để nhảy mượt (`scrollIntoView`) tới câu hỏi tương ứng, kích hoạt viền nhấp nháy highlight 1.2s. |
| **Modal kết quả (Score Modal)** | Pop-up Card + Analytics | Huy hiệu điểm số lớn tròn (thang 10), xếp loại học lực, thống kê số câu đúng/sai/bỏ qua, và thời gian hoàn thành. |
| **Khung đoạn văn (Passage)** | Card viền mỏng, typography thoáng | Chỗ trống `(N) _________` được đóng khung nổi bật; từ vựng gạch chân `<u>...</u>` được tạo style rõ ràng. |
| **Đáp ứng thiết bị (Responsive)** | Mobile-first & Fluid Layout | Hiển thị hoàn hảo trên Mobile, Tablet, Laptop, và Màn hình lớn 4K. |
| **Bảng câu hỏi Mobile (Bottom Sheet)** | Slide-up Sheet Drawer (8/5 cols) | Chạm nút "Ma Trận" hoặc thanh tiến độ hoặc FAB nổi để mở bảng 40 câu trượt từ dưới lên, chạm số câu để cuộn mượt đến ngay câu đó. |
| **Nút nổi điều hướng thông minh (FAB)** | `📋 Ma trận` & `↑ Lên đầu` | Tự động chuyển đổi khi vào tab Test, có đệm an toàn `95px` ở đáy trang tránh đè chữ. |
| **Đoạn văn đọc hiểu Mobile** | Left-aligned typography | Căn lề trái chống hiện tượng giãn cách từ thưa (rivers of whitespace) trên màn hình hẹp (360-420px). |

---

## 4. Công Cụ & Script Tự Động Hóa (Execution Pipeline)

Script tự động hóa lưu tại:
[`scripts/build_web_test.py`](file:///d:/GS10/.agent/skills/skills-web-test-portal/scripts/build_web_test.py)

### Cú pháp chạy lệnh:

1. **Sinh đề thi và tích hợp vào `index.html` cho một Unit (Mặc định Unit 1):**
```powershell
python ".agent\skills\skills-web-test-portal\scripts\build_web_test.py" --unit 1
```

2. **Chỉ sinh file HTML đề thi độc lập (`lessons/unit-<N>/test/test_unit<N>.html`):**
```powershell
python ".agent\skills\skills-web-test-portal\scripts\build_web_test.py" --unit 1 --standalone
```

### Các tham số hỗ trợ:
- `--unit <N>`: Số thứ tự Unit cần tạo đề thi (mặc định: `1`).
- `--workspace <path>`: Thư mục gốc chứa dự án (mặc định: `d:\GS10`).
- `--inject-index`: Tự động chèn tab, mục lục, CSS và JS vào `index.html` (mặc định: `True`).
- `--standalone`: Tự động xuất trang kiểm tra độc lập (mặc định: `True`).

---

## 5. Quy Trình Kiểm Định Chất Lượng (Quality Audit Checklist)

Trước khi nghiệm thu hoặc đẩy mã nguồn lên môi trường triển khai (Vercel), phải kiểm tra 8 tiêu chí sau:

1. **Kiểm tra cú pháp JavaScript (Zero Syntax Errors)**: Chạy `node --check` trên toàn bộ khối mã script trong file HTML để đảm bảo không có lỗi cú pháp.
2. **Đầy đủ 40 câu hỏi**: Đảm bảo cả Test 01 và Test 02 hiển thị đủ 40 câu hỏi, không bị khuyết câu nào.
3. **Đồng hồ đếm ngược hoạt động chính xác**: Bấm Bắt đầu / Tạm dừng / Đặt lại hoạt động đúng; tự động bắt đầu khi chọn câu hỏi đầu tiên.
4. **Chọn đáp án mượt mà**: Click vào thẻ phương án bất kỳ (A, B, C, D) cập nhật radio, đổi màu thẻ và đổi màu nút tương ứng trong Question Palette.
5. **Điều hướng Question Palette**: Click vào số câu trong Palette cuộn mượt đến đúng vị trí câu hỏi trên màn hình.
6. **Chấm điểm và nộp bài chính xác**:
   - Nếu còn câu chưa làm, hiển thị thông báo xác nhận.
   - Khi nộp bài: Dừng đồng hồ, hiển thị Modal điểm số đúng theo công thức `Điểm = Số_câu_đúng * 0.25`.
   - Hiển thị đầy đủ nhãn `✓ Đúng` và `✗ Sai` tại các câu hỏi.
7. **Hiển thị lời giải chi tiết**: Sau khi nộp bài hoặc bấm "Xem Đáp Án", toàn bộ khung giải thích phân loại kiến thức và dịch nghĩa tiếng Việt được hiển thị rõ ràng, chuẩn định dạng.
8. **Chuyển tab Test 01 & Test 02**: Chuyển đổi giữa 2 đề thi mượt mà, không xung đột dữ liệu trả lời và timer của nhau.
