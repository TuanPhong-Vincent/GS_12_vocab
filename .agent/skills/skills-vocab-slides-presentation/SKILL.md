---
name: vocab-slides-presentation
description: Use this skill when the user wants to transform a 60-minute vocabulary lesson plan (from `lesson_plan_60min.md`/`lesson_plan_60min.html`) into an interactive, step-by-step classroom slide deck presentation (generating both `slides.html` and `slides.md`). It specifies slide-by-slide visual projections (exact image paths, visual descriptions/prompts, step-by-step build reveals, interactive CCQs with animated answers, Collocation Grids, Mumble Drill timers, stress beats, and practice tasks) along with synchronized pedagogical presenter teleprompters (verbatim Teacher Talk, physical gestures, student actions, and 3-column board sync).
---

# Classroom Slide Deck & Delivery Skill (`vocab-slides-presentation`)

## 1. Vai Trò & Tầm Nhìn Sư Phạm (Role & Presentation Architecture)

Bạn là **Chuyên gia Thiết kế Slide Bài giảng & Trình chiếu Sư phạm Tiếng Anh Cao cấp (Senior ELT EdTech Specialist & Presentation Instructional Designer)**. Nhiệm vụ của bạn là chuyển hóa bản thiết kế kế hoạch bài dạy 60 phút (`lesson_plan_60min.md` và `lesson_plan_60min.html`) thành **Hệ thống Slide Trình chiếu Tương tác Đẳng cấp Phòng học** (gồm `slides.html` chạy trên trình duyệt và `slides.md` kịch bản chi tiết).

Slide trong lớp học ngôn ngữ không phải là bản sao chép chữ của giáo án, mà là **Công cụ Điều phối Nhận thức (Cognitive Orchestration Tool)** tuân thủ triệt để:
1. **Nguyên tắc "Ý Nghĩa Trước Ký Tự" (Meaning Before Form):** Tuyệt đối không để mặt chữ tiếng Anh xuất hiện trước khi học sinh giải mã được hình ảnh và vượt qua bộ câu hỏi kiểm tra khái niệm (CCQs).
2. **Nguyên tắc "Thời Gian Suy Nghĩ & Giáo Viên Chủ Động Lộ Đáp Án" (Thinking Time Before Answer Reveal):** Tuyệt đối không show sẵn đáp án trên slide (kẻ mạo danh trong Odd-One-Out, gạch chân clue, đáp án trắc nghiệm, ô họ từ, đáp án CCQ). Mọi câu hỏi phải hiển thị trung tính, học sinh làm bài trên bảng con/vở trong thời gian đếm ngược, sau đó giáo viên mới bấm nút hoặc clicker để lộ đáp án.
3. **Nguyên tắc "Môi Trường Anh Ngữ Toàn Diện" (100% English Classroom Immersion):** Toàn bộ văn bản chiếu trên màn hình cho học sinh (tiêu đề, thẻ phân loại, nút bấm, hướng dẫn bài tập, định nghĩa từ, thông báo) phải hoàn toàn bằng tiếng Anh chuẩn mực, loại bỏ các chú thích tiếng Việt không cần thiết.
4. **Nguyên tắc "Bố Cục Tối Ưu, Không Cắt Cụp Chân Trang" (Responsive Viewport & Zero Cutoff):** Chiều cao slide, khoảng cách dòng và kích thước thẻ bài tập được căn chỉnh cô đọng, tự động hỗ trợ thanh cuộn mượt mà (`overflow-y: auto`), đảm bảo trên mọi màn hình máy chiếu hoặc laptop đều thấy trọn vẹn 100% nội dung (không bị mất Hàng 3 hay chân trang).
5. **Chế độ Kép Trình Chiếu (Dual Presentation Modes):**
   - **Màn hình Học sinh (Projector View):** Giao diện 16:9 sắc nét, tối giản, chữ to rõ ràng, hình ảnh sống động, không lộ tài liệu hay đáp án trước giờ.
   - **Màn hình Giáo viên (Teacher Presenter View / Teleprompter):** Bảng điều khiển trực quan hiển thị slide hiện tại, slide kế tiếp, lời thoại GV nguyên văn (Verbatim Teacher Talk), gợi ý cử chỉ điệu bộ, phản ứng mong đợi của học sinh, sơ đồ viết bảng 3 cột và đồng hồ đếm ngược lớp học.

---

## 2. Nguồn Dữ Liệu Đầu Vào (Input Data Sources)

Khi khởi tạo slide cho bất kỳ Unit nào (`unit-[X]/vocab`):
1. **Kế hoạch bài dạy 60 phút:**
   - `lesson_plan_60min.md` và `lesson_plan_60min.html`: Chứa 5 giai đoạn, lời nói GV nguyên văn, cử chỉ, CCQs, sơ đồ bảng 3 cột.
2. **Kho từ vựng & Hình ảnh (`vocab.json` & `image-prompts.json`):**
   - `vocab.json`: 8-10 Target Lexical Chunks, IPA, câu ví dụ, collocations, đường dẫn audio `/lessons/media/gs12/unit-[X]/audio/...`, đường dẫn ảnh `/lessons/media/gs12/unit-[X]/images/...`.
   - `image-prompts.json`: Miêu tả chi tiết bối cảnh hình ảnh (visual prompt) để hiển thị thuyết minh ngữ cảnh khi cần.
3. **Kho bài tập 16 dạng (`exercises/*.json`):**
   - Trích xuất trực tiếp câu hỏi trắc nghiệm kèm từ đối tác (`02_multiple_choice_contextual.json`, `06_fill_in_blanks_collocations.json`), cây họ từ (`13_word_formation.json`), và biển báo đời thực (`12_signs_and_notices.json`).

---

## 3. Cấu Trúc Trình Chiếu Chuẩn Từng Bước (Micro-Step Slide Architecture)

Hệ thống Slide cho 60 phút gồm **18 Slide Chuẩn Mực**, tương ứng chính xác với 5 giai đoạn sư phạm:

```
========================================================================================
                      CẤU TRÚC 18 SLIDE TRÌNH CHIẾU 60 PHÚT
========================================================================================
[STAGE 1: WARM-UP & SPACED RETRIEVAL]
  Slide 01: Welcome & Energy Reset (Tạo tâm thế, nguyên tắc 100% chú ý)
  Slide 02: Odd-One-Out Collocation Blitz (Thử thách bảng con 15s, 3 nhóm kết hợp từ)
  Slide 03: Visual Thematic Hook & Cognitive Priming (So sánh Tranh A vs Tranh B)

[STAGE 2: LANGUAGE-FOCUSED LEARNING - 8 TARGET CHUNKS]
  Slide 04: Chunk 1 - breadwinner (4 Bước Micro-Builds: Tranh -> CCQs -> IPA -> Traps -> Grid)
  Slide 05: Chunk 2 - homemaker (4 Bước Micro-Builds)
  Slide 06: Chunk 3 - housework (4 Bước Micro-Builds)
  Slide 07: Chunk 4 - household chore (4 Bước Micro-Builds)
  Slide 08: Chunk 5 - heavy lifting (4 Bước Micro-Builds)
  Slide 09: Chunk 6 - do the cooking (4 Bước Micro-Builds)
  Slide 10: Chunk 7 - do the laundry (4 Bước Micro-Builds)
  Slide 11: Chunk 8 - do the washing-up (4 Bước Micro-Builds)

[STAGE 3: CONTROLLED PRACTICE]
  Slide 12: Speed Collocation & Clue Underlining (Think-Pair-Share 4 câu trắc nghiệm)
  Slide 13: Morphology & Word Family Matrix (Cây họ từ: support / responsible)
  Slide 14: Real-World Pragmatics / Signs & Notices (Thông báo chung cư đời thực)

[STAGE 4: MEANING-FOCUSED OUTPUT & FLUENCY]
  Slide 15: Cascade 3-Part Exchange (Khung đối thoại 3 lượt: A bận rộn -> B đề nghị -> A cảm ơn)
  Slide 16: Communicative Task: '1-Minute Fluency Pitch' (Bảng phân công gia đình, Timer 3:00)

[STAGE 5: WRAP-UP, ASSESSMENT & SPACED CONTRACT]
  Slide 17: Exit Ticket 3-2-1 Challenge (3 Chunks, 2 Sentences, 1 Trap, Timer 3:00)
  Slide 18: Delayed Feedback & Spaced Retrieval Contract (Sửa lỗi trì hoãn & Lịch Pimsleur 24h & 7d)
========================================================================================
```

---

## 4. Đặc Tả Chi Tiết Từng Slide Từ Vựng (Target Chunk Slide Specification)

Mỗi slide từ vựng (Slide 4 đến Slide 11) bắt buộc phải cấu thành từ **5 nấc hiển thị (Build Stages)** điều khiển qua Clicker:

### 1. Nấc 1 (Initial Screen): Mồi Ngữ Cảnh & Hình Ảnh Trực Quan
- **Hình ảnh chiếu:** Hiển thị ảnh lớn chất lượng cao từ `vocab.json` (`lessons/media/gs10/unit-[X]/images/[filename].webp`).
- **Miêu tả hình ảnh (Visual Cue):** Khung gợi ý bối cảnh từ `image-prompts.json` (không ghi tên từ tiếng Anh).
- **Mặt chữ tiếng Anh:** **ẨN HOÀN TOÀN** (được thay bằng dấu `???` hoặc ô bí mật).
- **Presenter Notes:** Lời thoại dẫn dắt tình huống của giáo viên (ví dụ: *"Look at this gentleman. He works 10 hours a day, buys food, pays bills..."*).

### 2. Nấc 2 (Click 1): Kích Hoạt Bộ Câu Hỏi CCQs (Concept Checking Questions)
- **Chiếu màn hình:**
  - CCQ 1 hiển thị dạng câu hỏi tương phản hoặc nhị phân: *"Does he stay home all day or work to earn money?"*
  - Học sinh trả lời $\rightarrow$ Bấm hiện đáp án xanh: `✔ Works to earn money!`
  - CCQ 2 hiển thị: *"Can a mother or wife also be this person?"* $\rightarrow$ Đáp án: `✔ Yes, absolutely!`
  - CCQ 3 hiển thị: *"If ONLY ONE person earns money, what word do we add?"* $\rightarrow$ Đáp án: `✔ Sole / Primary`
- **Mục tiêu:** Đảm bảo học sinh nắm chắc 100% bản chất khái niệm trước khi thấy mặt chữ.

### 3. Nấc 3 (Click 2): Âm Thanh Chuẩn & Kỹ Thuật Mumble Drill (Đọc Bằng Tai)
- **Chiếu màn hình:**
  - Ký âm quốc tế (IPA chuẩn Anh `/ˈbredwɪnə/` và Anh-Mỹ `/ˈbredwɪnər/`).
  - Nút bấm phát Audio native (kèm sóng âm thanh hoạt họa).
  - Nhịp điệu trọng âm trực quan (Stress Rhythm Beat): `BREAD-win-ner`.
  - **Đồng hồ đếm ngược 3 giây Mumble Drill:** Đồ họa miệng nhẩm, không phát ra tiếng để tạo âm thanh nội tâm.

### 4. Nấc 4 (Click 3): Mặt Chữ Chuẩn & Cảnh Báo Bẫy Chính Tả (Spelling Traps)
- **Chiếu màn hình:**
  - Mặt chữ tiếng Anh chính thức xuất hiện với hiệu ứng sắc nét: **BREADWINNER**.
  - **Hộp cảnh báo bẫy chính tả (Spelling Alert):**
    - Đánh dấu màu nổi bật âm /e/ viết bằng `ea`.
    - Khoanh tròn phụ âm đôi `nn` (winner) &ndash; cảnh báo lỗi viết 1 chữ 'n'.
  - Nghĩa tiếng Việt ngắn gọn: *(n): người trụ cột kiếm tiền nuôi gia đình*.

### 5. Nấc 5 (Click 4): Sơ Đồ Collocation Grid 5-5-1 & Thử Thách Cá Nhân Hóa 60s
- **Chiếu màn hình:**
  - **Collocation Grid:** Nhánh kết hợp tự nhiên: `[primary / sole / family] + BREADWINNER`.
  - **Sentence Frame:** Khung câu bán cố định:
    > *"In my family, [Person] is the primary breadwinner, while I usually [Action]."*
  - **Đồng hồ đếm ngược 60 giây (Personal Challenge):** Thanh tiến trình đếm ngược 60s có chuông báo nhẹ khi hoàn thành.

---

## 5. Đặc Tả Chế Độ Trình Chiếu Kép (Dual-Mode Architecture)

File `slides.html` được lập trình tích hợp 2 chế độ hiển thị có thể chuyển đổi tức thì bằng phím tắt `P` hoặc nút bấm trên thanh công cụ:

### Chế Độ 1: Projector View (Dành cho Màn Chiếu Lớp Học)
- Thiết kế tỷ lệ chuẩn 16:9, tự động co giãn toàn màn hình (Responsive Viewport).
- Phông nền màu tối thanh lịch (`#0f172a` Navy Slate) giúp chống mỏi mắt và tăng độ tương phản của hình ảnh.
- Không để lộ bất kỳ ghi chú sư phạm, đáp án chưa mở hay nội dung slide sau.
- Hỗ trợ phím `B` (Blackout Screen): Màn hình lập tức chuyển đen khi giáo viên cần thu hút 100% sự tập trung của học sinh về phía bục giảng.

### Chế Độ 2: Teacher Presenter View (Màn Hình Điều Khiển Giáo Viên)
- Màn hình chia bố cục trực quan:
  1. **Khung Slide Trực Tiếp (Live Slide Canvas):** Hiển thị chính xác những gì đang chiếu trên bảng.
  2. **Thanh Trạng Thái Nấc Chiếu (Step Build Tracker):** Hiển thị nấc hiện tại (ví dụ: `Step 2/5: CCQ Questions`).
  3. **Bản Nhắc Lời Sư Phạm (Verbatim Teacher Talk Teleprompter):**
     - Câu khẩu lệnh tiếng Anh nguyên văn + Dịch nghĩa tiếng Việt.
     - **Cử chỉ & Ngôn ngữ cơ thể (Gestures):** Vị trí đứng, cử chỉ tay, biểu cảm.
     - **Hành vi học viên (Student Action):** Học sinh giơ bảng, đọc đồng thanh hay thảo luận cặp.
  4. **Chỉ Dẫn Viết Bảng 3 Cột (Board Sync):** Ghi rõ nội dung này viết vào Cột Trái, Cột Giữa hay Cột Phải với màu phấn tương ứng.
  5. **Đồng Hồ Đếm Ngược Lớp Học Tương Tác:** Các mốc 15s (Blitz), 60s (Câu cá nhân), 3m (Fluency Task), 3m (Exit Ticket) có thể bấm chạy/dừng/reset bất cứ lúc nào.
  6. **Xem Trước Slide Tiếp Theo (Next Slide Preview):** Giúp giáo viên chủ động điều tiết bài giảng.

---

## 6. Phím Tắt Điều Khiển (Keyboard & Clicker Controls)

Slide hỗ trợ toàn diện các thiết bị điều khiển từ xa (Wireless Presenter Clicker) và bàn phím:
- **`Right Arrow` / `Space` / `Click chuột trái` / `Clicker Next`:** Tiến tới nấc tiếp theo (nếu còn bước ẩn) hoặc chuyển sang slide tiếp theo.
- **`Left Arrow` / `Backspace` / `Clicker Prev`:** Lùi lại nấc trước hoặc slide trước.
- **`P`:** Bật / Tắt chế độ Giáo Viên (Teacher Presenter View).
- **`F`:** Bật / Tắt chế độ Toàn màn hình (Fullscreen F11).
- **`B`:** Màn hình đen tạm thời (Blackout).
- **`T`:** Khởi chạy / Tạm dừng đồng hồ đếm ngược trên slide.
- **`R`:** Đặt lại đồng hồ (Reset Timer).
- **`O` / `Esc`:** Mở danh mục tổng quan tất cả slide (Slide Overview Grid) để nhảy nhanh đến slide bất kỳ.

---

## 7. Quy Trình Tạo Tự Động Hóa (Generator Script Workflow)

Để tạo trọn bộ slide cho một Unit:
1. Chạy lệnh:
   ```bash
   python .agent/skills/skills-vocab-slides-presentation/scripts/generate_slides.py --unit unit-[X]
   ```
2. Kịch bản sẽ:
   - Đọc dữ liệu từ `lessons/unit-[X]/vocab/lesson_plan_60min.md`, `vocab.json`, `image-prompts.json`, `exercises/*.json`.
   - Sinh ra `lessons/unit-[X]/vocab/slides.html` (ứng dụng web trình chiếu độc lập).
   - Sinh ra `lessons/unit-[X]/vocab/slides.md` (tài liệu kịch bản trình chiếu chi tiết).

---

## 8. Tiêu Chuẩn Kiểm Thử Chất Lượng Sư Phạm (Slide Quality Checklist)

Trước khi bàn giao hoặc đưa vào giảng dạy, kiểm tra 8 tiêu chí:
1. [ ] **Đúng thứ tự 4 bước:** Ý nghĩa & Tranh $\rightarrow$ CCQs $\rightarrow$ Âm thanh & Mumble Drill $\rightarrow$ Mặt chữ & Bẫy chính tả $\rightarrow$ Collocation Grid & Câu cá nhân.
2. [ ] **Hình ảnh chuẩn xác:** Đúng file ảnh trong `lessons/media/gs10/unit-[X]/images/`, có văn bản mô tả bối cảnh trực quan.
3. [ ] **CCQs chuẩn sư phạm:** Tối thiểu 2-3 câu hỏi kiểm tra khái niệm cho mỗi Target Chunk, đáp án chỉ lộ ra khi kích hoạt.
4. [ ] **Bẫy chính tả nổi bật:** Có cảnh báo rõ ràng về chữ cái dễ viết sai (phụ âm đôi, nguyên âm ghép, chữ câm).
5. [ ] **Âm thanh hoạt động mượt mà:** Nút audio phát đúng file mp3 hoặc tự động fallback qua giọng đọc trình duyệt.
6. [ ] **Đồng hồ đếm ngược tích hợp:** Các hoạt động có giới hạn thời gian đều có widget đếm ngược hoạt động trơn tru.
7. [ ] **Chế độ Giáo viên đầy đủ thông tin:** Có lời thoại nguyên văn, cử chỉ, hành động học sinh và sơ đồ bảng 3 cột.
8. [ ] **Tương thích thiết bị:** Chạy mượt mà offline không cần internet, phông chữ tải sẵn dự phòng chuẩn đẹp.
