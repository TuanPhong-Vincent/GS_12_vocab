# Quy Tắc Thiết Kế & Trình Chiếu CCQs Trên Màn Hình Slide

## 1. Định Nghĩa & Tầm Quan Trọng Của CCQs Trên Slide

**CCQs (Concept Checking Questions)** là các câu hỏi kiểm tra khái niệm nhằm xác minh học sinh hiểu đúng bản chất ngữ nghĩa của từ vựng mà không cần dịch thô sang tiếng mẹ đẻ.

Khi đưa CCQs lên màn hình trình chiếu:
- **Tuyệt đối không chiếu cả câu hỏi lẫn câu trả lời cùng một lúc.**
- **Tuyệt đối không chứa từ mục tiêu trong câu hỏi** (ví dụ: cấm hỏi *"Does a breadwinner win bread?"*).
- **Phải thiết kế hiệu ứng xuất hiện hai pha (Two-Phase Progressive Reveal):**
  - Pha 1: Câu hỏi xuất hiện $\rightarrow$ Giáo viên đọc to $\rightarrow$ Học sinh tư duy và trả lời miệng.
  - Pha 2: Bấm clicker $\rightarrow$ Đáp án chuẩn hiện ra với màu xanh lá (`#10b981`) kèm biểu tượng `✔` để củng cố nhận thức.

---

## 2. Bộ 4 Dạng Câu Hỏi CCQs Chuẩn Sư Phạm

### Dạng 1: Câu Hỏi Nhị Phân / Tương Phản (Binary / Contrastive Questions)
- **Mục đích:** Buộc người học phân định rõ hai thái cực hành vi hoặc đối tượng.
- **Ví dụ với *breadwinner*:**
  - *CCQ:* "Does he stay home all day or go out to work and earn money?"
  - *Reveal Key:* `✔ Goes out to work and earns money!`
- **Ví dụ với *household chore*:**
  - *CCQ:* "Is a chore a big annual event or a routine daily task?"
  - *Reveal Key:* `✔ A routine daily task!`

### Dạng 2: Câu Hỏi Giới Hạn Phạm Vi / Điều Kiện (Constraint & Boundary Questions)
- **Mục đích:** Xóa bỏ định kiến hoặc hiểu lầm về ngữ cảnh văn hóa/xã hội.
- **Ví dụ với *breadwinner*:**
  - *CCQ:* "Can a mother or wife also be the breadwinner?"
  - *Reveal Key:* `✔ Yes, absolutely! Modern families often have both.`
- **Ví dụ với *homemaker*:**
  - *CCQ:* "Can a man be a homemaker?"
  - *Reveal Key:* `✔ Yes! A househusband or stay-at-home dad.`

### Dạng 3: Câu Hỏi Ngữ Pháp & Ngữ Vựng Gắn Liền (Grammatical & Collocational Check)
- **Mục đích:** Ngăn ngừa lỗi ghép sai động từ (de-lexicalised verbs) hoặc danh từ đếm được/không đếm được.
- **Ví dụ với *housework*:**
  - *CCQ 1:* "Can we say 'I have many houseworks to do'?"
  - *Reveal Key:* `✔ No! Housework is uncountable. (Never add -s)`
  - *CCQ 2:* "Which verb goes with housework: MAKE or DO?"
  - *Reveal Key:* `✔ DO housework! (Never say make housework)`

### Dạng 4: Câu Hỏi Khối Ngữ Lưu Nâng Cao (Chunk Extension Question)
- **Mục đích:** Dẫn dắt trực tiếp vào tính từ đối tác (Collocation partner).
- **Ví dụ với *breadwinner*:**
  - *CCQ:* "If ONLY ONE person in the family earns money, what word do we add before breadwinner?"
  - *Reveal Key:* `✔ Sole breadwinner / Primary breadwinner`

---

## 3. Quy Chuẩn Hiển Thị Đồ Họa Của CCQs Trên Slide

```html
<!-- Cấu trúc HTML của một khối CCQ trên Slide -->
<div class="ccq-card" data-step="1">
    <div class="ccq-header">
        <span class="ccq-badge">CCQ 1</span>
        <span class="ccq-question">Does a breadwinner stay home all day or work to earn money?</span>
    </div>
    <div class="ccq-answer hidden">
        <span class="check-icon">✔</span> Works to earn money!
    </div>
</div>
```

- **Màu sắc câu hỏi:** Nền xanh đen nhạt (`#1e293b`), chữ trắng sáng (`#f8fafc`), viền xám nhạt (`#475569`).
- **Màu sắc đáp án khi bấm lộ ra:** Nền xanh lá đậm (`#064e3b`), chữ xanh ngọc sáng (`#6ee7b7`), viền xanh ngọc (`#10b981`), có animation fade-in và slide-down nhẹ nhàng.
- **Kích thước chữ:** Tối thiểu `18px - 20px` để học sinh ngồi ở bàn cuối lớp học vẫn nhìn rõ 100%.
