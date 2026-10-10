---
name: display-test
description: Use this skill when the user asks to display, format, layout, or export standardized 40-question English unit tests (e.g., test1.json, test2.json, or tests in lessons/unit-*/test/) into a publication-grade PDF exam paper matching official Vietnamese high school graduation exam standards (Arial 12pt, margin 0.5cm, pure B&W, dynamic 1/2/4-row option arrangement, continuous natural flow without artificial page breaks, title "UNIT * - TEST 0*", shortened bold question labels "1:", "2:", exact 6-page budget).
---

# Standard Unit Test Typesetting & PDF Export Skill (`display-test`)

## 1. Role & Purpose

Bạn là một **Chuyên gia Dàn trang Đề thi Chuẩn hoá THPT Quốc gia (Standardized Exam Typesetter & Print Layout Specialist)**. Nhiệm vụ của bạn là chuyển đổi dữ liệu đề thi trắc nghiệm 40 câu từ file JSON chuẩn (`test1.json`, `test2.json`,...) sang tài liệu PDF đề bài thi in ấn chuyên nghiệp, chuẩn mực sư phạm và thẩm mỹ cao nhất, lưu tại:
- `lessons/unit-<N>/test/test1.pdf` (hoặc `UNIT <N> - TEST 01.pdf`)
- `lessons/unit-<N>/test/test2.pdf` (hoặc `UNIT <N> - TEST 02.pdf`)

---

## 2. Tiêu Chuẩn Định Dạng Bắt Buộc (Strict Layout Standards)

| Thuộc tính | Quy chuẩn bắt buộc | Chi tiết kỹ thuật |
| :--- | :--- | :--- |
| **Phông chữ (Font)** | **Arial** | `font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;` |
| **Cỡ chữ (Font Size)** | **12pt** (Mặc định chuẩn) | Cỡ chữ chuẩn 12 cho toàn bộ nội dung câu hỏi, đoạn văn, và đáp án (tối ưu ngân sách trang in). |
| **Nhãn câu hỏi (Labels)** | **"1:", "2:", ... "40:" in đậm** | Thay thế toàn bộ "Question 1:", "Question 2:" thành **"1:"**, **"2:"** để tiết kiệm diện tích ngang tối đa. |
| **Tiêu đề (Title)** | **Chỉ duy nhất "UNIT * - TEST 0*"** | Không thêm tiêu đề phụ hay metadata thừa. VD: `UNIT 1 - TEST 01`, `UNIT 1 - TEST 02`. Chữ in hoa, in đậm, căn giữa (15pt bold). |
| **Màu sắc (Colors)** | **Trắng / Đen cổ điển** | Nền trắng thuần (`#ffffff`), chữ đen thuần (`#000000`), không màu mè, chuẩn đề thi THPT, tiết kiệm mực in. |
| **Lề trang (Margins)** | **0.5 cm x 0.5 cm x 0.5 cm x 0.5 cm** | Căn lề hẹp: `@page { size: A4 portrait; margin: 0.5cm; }`. |
| **Khoảng cách dòng (Line Height)** | **Vừa đủ, thoáng mắt** | `line-height: 1.25;` (đảm bảo độ tách bạch, không dính sát và không dãn thừa). |
| **Khoảng cách câu hỏi (Question Spacing)** | **6.0pt thoáng mắt** | `margin-bottom: 6.0pt;` trên `.question-item` và `margin-bottom: 2.5pt;` trên `.q-stem-text`, đảm bảo các câu hỏi tách bạch rõ ràng, không bị dính sát nhau mà vẫn duy trì chuẩn xác ngân sách 6 trang in. |
| **Khoảng cách hàng đáp án (Options Row Gap)** | **2.2pt thoáng đãng** | `row-gap: 2.2pt;` trên `.options-2rows` và `.options-4rows`, giúp các phương án trắc nghiệm không bị chật chội. |
| **Dòng chảy liên tục (Continuous Flow)** | **Không gượng ép ngắt trang** | Nội dung trải dài liên tục từ trang 1 đến trang 6, không chèn ngắt trang tùy tiện (`page-break-before: always`). Tận dụng trọn vẹn diện tích từng trang A4. |
| **Ngân sách trang (Page Budget)** | **Đúng 6 trang in** | Toàn bộ 40 câu hỏi trắc nghiệm cùng các bài đọc hiểu khớp trọn vẹn trong **6 trang A4**. Trang 6 kết thúc cân đối với các câu đọc hiểu cuối và `--- THE END ---`. |
| **Chống mồ côi (No Orphans)** | **Bảo vệ toàn vẹn câu hỏi** | `break-inside: avoid;` cho từng câu hỏi (thân câu hỏi và 4 đáp án không bị tách đôi ở mép trang). Tiêu đề đoạn văn và lời dẫn phần thi luôn gắn liền với nội dung bên dưới (`break-after: avoid;`). |

---

## 3. Quy Tắc Dàn 4 Phương Án A, B, C, D (Dynamic Options Arrangement)

Hệ thống tự động đo độ dài thực tế của từng chuỗi phương án theo kích thước font Arial 12pt (thông qua engine typography PyMuPDF) để quyết định cấu trúc lưới (grid) hiển thị:

1. **Dạng 1 Hàng (4 Cột - `options-1row`):**
   - Áp dụng khi 4 phương án ngắn (từ đơn, cụm từ ngắn, chuỗi ký tự sắp xếp như `a-c-b`, `Paragraph 1`, `was designed`, `communication`,...).
   - Hiển thị cả 4 đáp án `A.`, `B.`, `C.`, `D.` trên **1 dòng duy nhất**.
   - Tuyệt đối không để phương án nào bị rớt dòng đơn lẻ.
   
2. **Dạng 2 Hàng (2 Cột x 2 Hàng - `options-2rows`):**
   - Áp dụng khi độ dài phương án ở mức trung bình (cụm danh từ, ngữ động từ dài như `family advanced technology`, `Cooking meals together`, `attract beneficial insects`,...).
   - Hàng 1 gồm: `A.` và `B.`.
   - Hàng 2 gồm: `C.` và `D.`, căn lề thẳng đứng khớp 100% với cột của `A.` và `B.`.

3. **Dạng 4 Hàng (1 Cột x 4 Hàng - `options-4rows`):**
   - Áp dụng khi phương án dài (mệnh đề hoàn chỉnh, câu văn dài trong các bài đọc hiểu hoặc điền câu như Q18–Q22, Q27, Q28, Q34, Q37–Q40).
   - Mỗi phương án chiếm **1 dòng độc lập**, thẳng hàng từ trên xuống dưới.

---

## 4. Công Cụ & Script Thực Thi (Execution Pipeline)

Script tự động hoá được lưu trữ tại:
[`scripts/export_test_pdf.py`](file:///d:/GS10/.agent/skills/skills-display-test/scripts/export_test_pdf.py)

### Cú pháp dòng lệnh:

1. **Xuất PDF cho toàn bộ các đề thi trong thư mục Unit (Mặc định 12pt, 6 trang):**
```powershell
python "d:\GS10\.agent\skills\skills-display-test\scripts\export_test_pdf.py" "d:\GS10\lessons\unit-1\test" --preview
```

2. **Xuất PDF cho 1 đề thi cụ thể:**
```powershell
python "d:\GS10\.agent\skills\skills-display-test\scripts\export_test_pdf.py" "d:\GS10\lessons\unit-1\test\test1.json" --preview
```

3. **Tùy chỉnh cỡ chữ nếu cần (VD: 14pt):**
```powershell
python "d:\GS10\.agent\skills\skills-display-test\scripts\export_test_pdf.py" "d:\GS10\lessons\unit-1\test" --font-size 14.0
```

### Các tham số hỗ trợ:
- `target`: Đường dẫn tới file `test*.json` hoặc thư mục chứa đề thi.
- `--preview`: Xuất kèm các ảnh chụp màn hình chất lượng cao (PNG 150 DPI) cho từng trang trong thư mục `preview_test*` để phục vụ audit trực quan.
- `--output-dir`: (Tùy chọn) Thư mục xuất file PDF đích.
- `--font-size`: Cỡ chữ (mặc định: `12.0`).

---

## 5. Quy Trình Kiểm Định Chất Lượng (Quality Audit Checklist)

Trước khi bàn giao kết quả cho người dùng, Agent phải thực hiện kiểm định qua 7 tiêu chí:

1. **Tiêu đề duy nhất**: Đảm bảo tiêu đề ở đầu trang 1 là `UNIT <N> - TEST <01|02>`. Không có bất kỳ dòng chữ giới thiệu hay nhãn thừa nào phía trên hoặc dưới tiêu đề.
2. **Typography & Nhãn**: Font Arial cỡ chữ 12pt sắc nét. Các câu hỏi đánh số dạng **`1:`**, **`2:`**, ... **`40:`** in đậm.
3. **Căn lề**: Lề trang chuẩn 0.5cm ở cả 4 cạnh, khoảng cách lề đều đặn.
4. **Không ngắt trang tùy tiện**: Nội dung chảy liên tục từ trang 1 đến trang 6. Các đoạn văn đọc hiểu và câu hỏi kết nối tự nhiên.
5. **Không mồ côi (No split/orphan items)**:
   - Không có trường hợp câu hỏi bị ngắt đôi (thân câu ở cuối trang, đáp án ở đầu trang sau).
   - Không có trường hợp lời dẫn hoặc tiêu đề bài đọc nằm trơ trọi ở đáy trang mà không có nội dung kèm theo.
6. **Không rớt dòng đáp án**: Các đáp án trên cùng 1 hàng không bị co ép khiến chữ rớt dòng đơn lẻ.
7. **Ngân sách 6 trang in hoàn hảo**: Toàn bộ bài thi 40 câu kết thúc trọn vẹn ở trang 6 (Trang 6 chứa các câu 38–40 và `--- THE END ---`), tuyệt đối không bị tràn sang trang thứ 7.
