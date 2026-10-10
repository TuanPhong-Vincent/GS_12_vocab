# Global Success 12 - Vocabulary & Exercises Portal

Hệ thống web học và luyện tập từ vựng tiếng Anh chuẩn chương trình **Global Success 12**, bao gồm lý thuyết từ vựng trực quan (Flashcards Modern Blue) và toàn bộ 16 dạng bài tập trắc nghiệm & tự luận tương tác.

---

## 🌟 Tính Năng Nổi Bật

1. **Lý Thuyết Từ Vựng Trực Quan (`cards.html` & `index.html`)**:
   - Thiết kế chuẩn Modern Blue với typography hiện đại (*Plus Jakarta Sans* & *Be Vietnam Pro*).
   - Lưới hiển thị 4–5 thẻ/hàng trên desktop, tự động co giãn thông minh trên tablet và mobile.
   - Khung hình ảnh chuẩn tỷ lệ, không bị crop mất góc.
   - Nút phát âm trực quan tích hợp **Web Speech API** giọng chuẩn Mỹ (`en-US`).
   - Phiên âm chuẩn quốc tế IPA và nghĩa tiếng Việt đầy đủ.

2. **Lý Thuyết & Bài Tập Ngữ Pháp Chuẩn SGK (`grammar_unit*.html` & `index.html`)**:
   - **Lý thuyết chuẩn nhận diện SGK**: Đường kẻ xanh đầu bài (`border-top: 3px solid #1e40af`), Pill badges phân đoạn (`#e0f2fe`), bảng cấu trúc xanh Navy `#1e3a8a` với từ trọng tâm in đậm, hộp cảnh báo `⚠ WATCH OUT!`.
   - **8 Dạng bài tập ngữ pháp thực hành (A–H)**: Chia động từ, trắc nghiệm, nối vế câu, viết lại câu, điền từ đoạn văn, tìm lỗi sai, kết hợp câu, viết câu từ gợi ý.

3. **Hệ Thống 16 Dạng Bài Tập Từ Vựng Thực Hành**:
   - **Màu sắc đồng nhất**: Toàn bộ tiêu đề bài tập sử dụng bảng màu Navy sang trọng (`#1e3a8a` / `#2563eb`), bố cục gọn gàng, cân đối.
   - **Các dạng bài tập đa dạng**:
     - *01–03*: Trắc nghiệm trực tiếp, hoàn thành câu, hội thoại đối thoại.
     - *04*: Nhìn tranh đoán từ (Picture to Word).
     - *05*: Viết từ tiếng Anh từ nghĩa tiếng Việt.
     - *06–07*: Điền từ vào câu và đoạn văn có hộp từ gợi ý (Word Box).
     - *08*: Sắp xếp thứ tự các câu thành đoạn văn logic.
     - *09–10*: Tìm từ đồng nghĩa & trái nghĩa (Closest / Opposite Meaning).
     - *11*: Bài tập phân tích từ điển kiểu Oxford (Dictionary Entries).
     - *12*: Đọc hiểu biển báo & thông báo công cộng (Signs and Notices).
     - *13–15*: Bảng gia đình từ (Word Families Table), trắc nghiệm biến đổi từ và cấu tạo từ (Word Formation).
     - *16*: Dịch câu Việt – Anh (Sentence Translation).

4. **Chế Độ Học Tập Kép (Dual Modes)**:
   - **👁️ Xem Đáp Án (Review Mode)**: Hiển thị ngay đáp án đúng, tích xanh trực quan dành cho giáo viên và kiểm duyệt.
   - **✏️ Làm Bài (Practice Mode)**: Làm bài trực tiếp trên trình duyệt, chấm điểm tự động và tính % độ chính xác.
   - **🔍 Tìm kiếm trực tiếp**: Lọc từ vựng và câu hỏi theo thời gian thực.
   - **🖨️ Xuất bản & In ấn**: Tối ưu sẵn cho in ra giấy hoặc xuất PDF worksheets 11 trang chuẩn mực.

---

## 🚀 Cấu Trúc Thư Mục

```text
├── index.html                  # Master Web Portal (Lý thuyết Cards + 16 Dạng bài tập Vocab + Lý thuyết & 8 Dạng bài tập Grammar)
├── cards.html                  # Trang thẻ từ vựng độc lập (Flashcards Modern Blue)
├── GS12.pdf                    # Sách giáo khoa tiếng Anh 12 chuẩn Global Success (155 trang)
├── lessons/                    # Dữ liệu các bài học theo Unit
│   ├── unit-1/                 # Unit 1: Life Stories We Admire (vocab/, grammar/, grammar_unit1.html)
│   ├── unit-2/                 # Unit 2: A Multicultural World (vocab/, grammar/, grammar_unit2.html)
│   ├── unit-3/                 # Unit 3: Green Living (vocab/, grammar/, grammar_unit3.html)
│   └── media/                  # Kho tài nguyên hình ảnh bài học
└── .agent/skills/              # Bộ kỹ năng tự động hóa Antigravity Skills (18 skills chuẩn hóa GS12)
```

---

## 🌐 Triển Khai Lên Web (GitHub Pages)

1. Vào **Settings** của repository trên GitHub.
2. Chọn mục **Pages** (ở cột bên trái).
3. Tại **Build and deployment > Branch**, chọn branch `main` và thư mục `/(root)`.
4. Nhấn **Save**. Website sẽ tự động xuất bản tại:
   `https://TuanPhong-Vincent.github.io/gs12-vocab-portal/`
